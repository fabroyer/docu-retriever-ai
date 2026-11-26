"""
Document retrieval service.
Retrieves relevant document chunks from ChromaDB.
"""

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Chroma configuration
BASE_DIR = Path(__file__).resolve().parents[2]
PERSIST_DIRECTORY = str(BASE_DIR / "chroma_db")
COLLECTION_NAME = "documents"

# Initialize embedding model
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

def get_retriever():
    """Connect to ChromaDB and return a hybrid retriever"""

    vector_store = Chroma(
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=PERSIST_DIRECTORY,
    )

    # Retrieve documents for BM25
    # Second "document" is the key for the dictionnary created by .get with document's text inside
    # We have a list of textual content
    document_texts = vector_store.get(include=["documents"])["documents"]

    vector_retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 5, "fetch_k": 15}
    )

    bm25_retriever = BM25Retriever.from_texts(
        document_texts,
        k=5
    )

    ensemble_retriever = EnsembleRetriever(
        retrievers=[vector_retriever, bm25_retriever],
        weights=[0.5, 0.5]
    )

    return ensemble_retriever

def test_search(query):
    vector_store = Chroma(
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=PERSIST_DIRECTORY,
    )

    results = vector_store.similarity_search_with_score(
        query,
        k=5
    )

    for document, score in results:
        print("\nScore:", score)
        print(document.page_content[:500])