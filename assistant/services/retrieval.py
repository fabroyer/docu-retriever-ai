"""
Document retrieval service.
Retrieves relevant document chunks from ChromaDB.
"""

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

# Chroma configuration
PERSIST_DIRECTORY = "chroma_db"
COLLECTION_NAME = "documents"

# Initialize embedding model
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

def get_retriever():
    """Connect to ChromaDB and return a retriever"""

    vector_store = Chroma(
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=PERSIST_DIRECTORY,
    )

    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 3, "fetch_k": 10}
    )

    return retriever