from langchain_community.chat_models import ChatZhipuAI
from configs import constants
import os
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_openai import AzureChatOpenAI
from langchain_deepseek import ChatDeepSeek



def init_dsv3_model():
    llm = ChatDeepSeek(
        model_name="deepseek-v3",
        api_key=constants.__API_KEY,
        api_base=constants.__CUSTOM_API_URL,
        request_timeout=600
    )
    return llm


# init_text_to_vec_ch初始化中文嵌入层
def init_hugging_face_embedding(model_name: str, encode_kwargs: str): 
    embeddings = HuggingFaceBgeEmbeddings(
        model_name=constants.EMBEDDING_MODEL_NAME,
        encode_kwargs=constants.ENCODE_KWARGS
    )
    return embeddings
        

def init_chatgpt_model():
    os.environ["AZURE_OPENAI_API_KEY"] = constants.AZURE_OPENAI_API_KEY
    model = AzureChatOpenAI(
        azure_endpoint=constants.AZURE_ENDPOINT,
        azure_deployment=constants.AZURE_MODEL,
        openai_api_version=constants.API_VERSION,
        temperature=0.5,
    )
    return model