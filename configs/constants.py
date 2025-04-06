#langsmith
LANGCHAIN_TRACING_V2 = "true"

LANGCHAIN_PROJECT="test"

# 嵌入层相关
EMBEDDING_MODEL_NAME = "./text2vec-base-chinese"
ENCODE_KWARGS = {'normalize_embeddings': True}

# mysql
MYSQL_URI = "mysql+pymysql://root:xjf_dev_123456_...@120.79.179.187:3306/test"

# milvus参数
# MILVUS_HOST = "standalone" # 部署docker compose时使用?
MILVUS_HOST = "127.0.0.1"
MILVUS_PORT = "19530"

__API_KEY = ""
__CUSTOM_API_URL = ""

LANGCHAIN_API_KEY=""
AZURE_OPENAI_API_KEY="" 
AZURE_MODEL=""
AZURE_ENDPOINT=""
API_VERSION=""

# mysql
MYSQL_URI = ""