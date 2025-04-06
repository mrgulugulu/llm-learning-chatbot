from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from configs import constants
from langchain_milvus import Milvus

#  import_vectors_from_doc 将文档转向量存入milvus
def import_vectors_from_doc(documents: list):
    embeddings = HuggingFaceBgeEmbeddings(
    model_name=constants.EMBEDDING_MODEL_NAME,
    encode_kwargs=constants.ENCODE_KWARGS
)
    #TODO: 修改这里召回器返回内容，源文件在
    # 环境地址/lib/python3.12/site-packages/langchain_chroma/vectorstores.py
    _ = Milvus.from_documents(
        documents,
        embedding=embeddings,
        collection_name="test",
        connection_args={"host": constants.MILVUS_HOST, "port": constants.MILVUS_PORT},
        drop_old=True
    )



if __name__ == '__main__':
    import_vectors_from_doc([])
    