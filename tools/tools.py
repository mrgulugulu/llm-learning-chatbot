from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from configs import constants
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from datetime import datetime, timedelta
from langchain.tools.retriever import create_retriever_tool
from langchain.retrievers.self_query.base import SelfQueryRetriever
from tools.milvus import Milvus 
import json
from typing import Optional
from langchain_core.tools import tool
from configs import prompts, base_models
from langchain_core.output_parsers import StrOutputParser
from typing import Optional, Dict, List
from test import fake_data


def get_self_query_retriever_tool(llm, documents: list, metadata_field_info, document_content_description):
    embeddings = HuggingFaceBgeEmbeddings(
    model_name=constants.EMBEDDING_MODEL_NAME,
    encode_kwargs=constants.ENCODE_KWARGS
)
    #TODO: 修改这里召回器返回内容，源文件在
    # 环境地址/lib/python3.12/site-packages/langchain_milvus/vectorstores/milvus.py 1091行开始
    vectorstore = Milvus.from_documents(
        documents,
        embedding=embeddings,
    )
    retriever = SelfQueryRetriever.from_llm(
        llm,
        vectorstore,
        document_content_description,
        metadata_field_info,
    )
    retriever_tool = create_retriever_tool(
    retriever,
    name="教学问答信息召回器",
    description="对原问题的扩展",
    )
    return retriever_tool


@tool
def extract_keywords(text: str) -> str:
    """Extract keywords from the given text. Specify language for better results."""
    
    # 定义查询prompt（可根据需要调整）
    query_prompt = prompts.get_system_prompt_set_prompt(prompts.decompose_query_prompt)
    llm = base_models.init_dsv3_model()
    # 构建chain
    fetch_keywords_chain = query_prompt | llm | StrOutputParser()
    
    # 执行chain
    result = fetch_keywords_chain.invoke({
        "input": text,
    })
    
    return result


@tool
def retrieve_documents(query: str, top_k: int = 1) -> List[str]:
    """
    检索与查询相关的文档片段
    参数:
        query: 查询文本
        top_k: 返回的文档数量
    """
    retriever = get_simple_top_k_retriever_from_doc(documents=fake_data.qa_examples_using_topic_expansion_as_page_content,top_k=1)
    docs = retriever.invoke(query, top_k=top_k)
    return [doc.page_content for doc in docs]



@tool
def rag_qa_tool(input: str, context: Optional[str] = None) -> Dict:
    """
    使用RAG (Retrieval-Augmented Generation) 回答用户问题。
    参数:
        question: 用户的问题
        context: 可选的上下文信息 (如检索到的文档片段)
    返回:
        包含答案和来源的字典
    """
    # 获取系统预设的RAG提示模板
    rag_qa_prompt = prompts.get_system_prompt_set_prompt(prompts.topic_expansion_prompt_v2.format(school_id=125, context="{context}", teacher_id=1))
    llm = base_models.init_dsv3_model()
    # 构建RAG Chain
    rag_chain = (
        {"input": lambda x: x["input"], 
         "context": lambda x: x.get("context", "无额外上下文")}
        | rag_qa_prompt
        | llm
        | StrOutputParser()
    )
    
    # 执行Chain
    answer = rag_chain.invoke({
        "input": input,
        "context": context
    })
    
    return {
        "answer": answer,
        "sources": context if context else "无来源信息"
    }

def get_common_time_list(query: str) -> str:
    """get common time list, such as what day is it last weekend"""
    # 获取当前日期和时间
    current_datetime = datetime.now()
    # 格式化当前日期和时间
    formatted_time = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    # 返回格式化后的当前时间
    # 计算上个周末的日期
    # 获取当前日期
    today = datetime.now()

    # 计算当前日期是星期几（0=周一, 6=周日）
    weekday = today.weekday()

    # 计算上个周六的日期
    last_saturday = today - timedelta(days=weekday + 2)

    # 计算上个周日的日期
    last_sunday = today - timedelta(days=weekday + 1)
    
    # 计算近两周的日期
    start_of_week_1 = today - timedelta(days=(today.weekday() + 7))  # 上周一
    end_of_week_1 = start_of_week_1 + timedelta(days=6)  # 上周日

    # 第二周
    start_of_week_2 = start_of_week_1 + timedelta(days=7)  # 本周一
    end_of_week_2 = start_of_week_2 + timedelta(days=6)  # 本周日
    time_dict = {
        "当前时间": formatted_time,
        "上周六": last_saturday.strftime('%Y-%m-%d'),
        "上周日": last_sunday.strftime('%Y-%m-%d'),
        "近两周的第一周周一": start_of_week_1.strftime('%Y-%m-%d'),
        "近两周的第一周周日": end_of_week_1.strftime('%Y-%m-%d'),
        "近两周的第二周周一": start_of_week_2.strftime('%Y-%m-%d'),
        "近两周的第二周周日": end_of_week_2.strftime('%Y-%m-%d'),
    }
    json_string = json.dumps(time_dict, ensure_ascii=False, indent=4)
    return f"common time list: {json_string}"


# get_simple_top_k_retriever 简单topk召回器，从milvus获取
def get_simple_top_k_retriever(top_k: int):
    embeddings = HuggingFaceBgeEmbeddings(
    model_name=constants.EMBEDDING_MODEL_NAME,
    encode_kwargs=constants.ENCODE_KWARGS
)
    #TODO: 修改这里召回器返回内容，源文件在
    # 环境地址/lib/python3.12/site-packages/langchain_milvus/vectorstores/milvus.py 1091行开始
    formatted_uri = f"http://{constants.MILVUS_HOST}:{constants.MILVUS_PORT}"
    # embeddings = OpenAIEmbeddings(model=constants.EMBEDDING_MODEL_NAME,)
    vector_store = Milvus(
        embedding_function=embeddings,
        connection_args={"uri": formatted_uri},
    )

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": top_k},
    )
    
    return retriever

# get_simple_top_k_retriever_from_doc 简单topk召回器, 并将文档存入milvus
def get_simple_top_k_retriever_from_doc(documents: list, top_k: int):
    embeddings = HuggingFaceBgeEmbeddings(
    model_name=constants.EMBEDDING_MODEL_NAME,
    encode_kwargs=constants.ENCODE_KWARGS
)
    formatted_uri = f"http://{constants.MILVUS_HOST}:{constants.MILVUS_PORT}"
    #TODO: 修改这里召回器返回内容，源文件在
    # 环境地址/lib/python3.12/site-packages/langchain_milvus/vectorstores/milvus.py 1091行开始
    vectorstore = Milvus.from_documents(
        documents,
        embedding=embeddings,
        collection_name="test",
        # connection_args={"uri": formatted_uri},
        connection_args={"host": constants.MILVUS_HOST, "port": constants.MILVUS_PORT}, # 本地调用时使用
        drop_old=True
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": top_k},
    )
    return retriever


# get_simple_top_k_retriever_tool 简单topk召回器工具
def get_simple_top_k_retriever_tool(documents: list, top_k: int):
    retriever = get_simple_top_k_retriever(documents, top_k)
    retriever_tool = create_retriever_tool(
    retriever,
    name="教学问答信息召回器",
    description="教学问答信息扩展器，该工具在流程中只能使用一次",
    )
    return retriever_tool


def get_bm25_retriever_tool(documents: list, top_k: int, name, desc):
    bm25_retriever = get_bm25_retriever(documents, top_k)
    bm25_retriever_tool = create_retriever_tool(
    bm25_retriever,
    name=name,
    description=desc,
    )
    return bm25_retriever_tool


# bm25_retriever 使用tfidf+向量相似的文件召回器
def get_bm25_retriever(documents: list, top_k: int):
    embeddings = HuggingFaceBgeEmbeddings(
    model_name=constants.EMBEDDING_MODEL_NAME,
    encode_kwargs=constants.ENCODE_KWARGS
    )
    vectorstore = Milvus.from_documents(
        documents,
        embedding=embeddings,
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": top_k},
    )
    embeddings = HuggingFaceBgeEmbeddings(
        model_name=constants.EMBEDDING_MODEL_NAME,
        encode_kwargs=constants.ENCODE_KWARGS
    )
    doc_list = [doc.page_content for doc in documents]
    bm25_retriever = BM25Retriever.from_texts(
        doc_list, metadatas=[{"source": f"BM25"}] * len(doc_list)
    )
    bm25_retriever.k = top_k
    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, retriever], weights=[0.5, 0.5]
    )
    return ensemble_retriever

