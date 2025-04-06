from langchain_core.messages import HumanMessage,SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
import os
from tools import tools
from configs import base_models, constants, prompts
from test import fake_data
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
import asyncio
from flask_socketio import SocketIO, emit
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter


store = {}
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

os.environ["LANGCHAIN_TRACING_V2"] = constants.LANGCHAIN_TRACING_V2
os.environ["LANGCHAIN_API_KEY"] = constants.LANGCHAIN_API_KEY


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# build_rag_retreiver_chain_v2 在rag之前在加一个llm进行提取关键字
def build_rag_retreiver_chain_v2(docs: list, school_id: str, teacher_id: str):
    llm = base_models.init_dsv3_model()
    
    formatted_prompt = prompts.topic_expansion_prompt_v2.format(school_id=school_id, context="{context}", teacher_id=teacher_id)
    rag_qa_prompt = prompts.get_system_prompt_set_prompt(formatted_prompt)
    
    query_prompt = prompts.get_system_prompt_set_prompt(prompts.decompose_query_prompt)
    fetch_keywords_chain = query_prompt | llm | StrOutputParser()


    retriever = tools.get_simple_top_k_retriever_from_doc(documents=docs,top_k=1)
    
    topic_expansion_chain = (
        {"context": {"input": itemgetter("input") | fetch_keywords_chain | retriever | format_docs}, "input": RunnablePassthrough()}
        | rag_qa_prompt
        | llm
        | StrOutputParser()
    )
    return topic_expansion_chain
    

def build_chat_agent():
    
    llm = base_models.init_chatgpt_model()
    memory = MemorySaver()
    
    retriever = tools.get_simple_top_k_retriever_from_doc(documents=fake_data.qa_examples_using_topic_expansion_as_page_content,top_k=1)

    db = SQLDatabase.from_uri(constants.MYSQL_URI)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    sql_tools = toolkit.get_tools()
    sql_tools.append(tools.get_common_time_list)
    sql_tools.append(tools.extract_keywords)
    sql_tools.append(tools.retrieve_documents)
    sql_tools.append(tools.rag_qa_tool)

    system_message = SystemMessage(content=prompts.CH_SQL_PREFIX)
    agent_executor = create_react_agent(llm, sql_tools, messages_modifier=system_message, checkpointer=memory)
    
    return agent_executor



# 流式输出
def graph_stream(graph, user_input: str, config):
    inputs = {"messages": [HumanMessage(content=user_input), 
                       SystemMessage(content=prompts.teacher_qa_system_prompt)]}
    for event in graph.stream(inputs, config, stream_mode="values"):
        message = event["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

async def graph_stream_with_token(graph, user_input: str, config):
    inputs = {
        "messages": [
            HumanMessage(content=user_input), 
            SystemMessage(content=prompts.teacher_qa_system_prompt)
        ],
        # "tool_choice": {"type": "function", "function": {"name": "extract_keywords"}}
    }
    async for event in graph.astream_events(inputs, config=config, version="v1"):
        kind = event["event"]
        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                # 使用 Socket.IO 实时发送内容到前端
                print(content, end = '', flush=True)
                
def learning_llm_chatbot_server(input: str, prompt):
    session_id = "abc124"
    config = {"configurable": {"thread_id": session_id}}
    rag_chain = build_rag_retreiver_chain_v2(fake_data.question_answers_examples, "125", "23")
    agent = build_chat_agent()
    
    topic_expansions = rag_chain.invoke(
        {"input": input},
        # config={"configurable": {"session_id": session_id}}
    )
    
    # 调用流式函数
    res = graph_invoke_with_prompt(agent, topic_expansions, config, prompt)
    return res
    
# 非流式输出
def graph_invoke(graph, user_input: str, config):
    inputs = {"messages": [HumanMessage(content=user_input), 
                       SystemMessage(content=prompts.teacher_qa_system_prompt)]}
    messages = graph.invoke(inputs, config) 
    message = messages["messages"][-1]
    return message.content

# 输入prompt的非流式输出
def graph_invoke_with_prompt(graph, user_input: str, config, system_msg_prompt: str):
    inputs = {"messages": [HumanMessage(content=user_input), 
                       SystemMessage(content=system_msg_prompt)]}
    messages = graph.invoke(inputs, config) 
    message = messages["messages"][-1]
    return message.content


async def main():
    session_id = "abc124"
    config = {"configurable": {"thread_id": session_id}}
    agent = build_chat_agent()
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            # 使用 await 调用异步函数
            await graph_stream_with_token(agent, user_input, config)
        
        except Exception as e:
            print(f"error: {e}")

if __name__ == '__main__':
    asyncio.run(main())

