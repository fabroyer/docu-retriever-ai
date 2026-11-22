"""
Document indexing service.
This module splits PDF documents into chunks, generates embeddings and stores them in ChromaDB.
"""

import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

# Load environment variables
load_dotenv()

# ChromaDB configuration
BASE_DIR = Path(__file__).resolve().parent[2]
PERSIST_DIRECTORY = str(BASE_DIR / "chroma_db")
COLLECTION_NAME = "documents"

# Initialize the embedding model
embeddings = OpenAIEmbeddings(model='text-embedding-3-small')

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)

def index(pages):
    """Split pages into chunks and stores them in ChromaDB."""

    # Split documents into chunks
    chunks = text_splitter.split_documents(pages)

    # Store chunks and embeddings into ChromaDB
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY,
        collection_name=COLLECTION_NAME,
    )

    print("Document indexing complete")

    return vector_store