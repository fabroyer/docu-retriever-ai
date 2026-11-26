"""
RAG service.
Generates answers based on retrieved documents chunks.
"""

from operator import itemgetter

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from assistant.services.retrieval import get_retriever

# Initialize the language model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Create the prompt
prompt = ChatPromptTemplate.from_template("""
Answer the question using only the information contained in the context.
If the context does not contain enough information to answer, say that you don't know.

Conversation history: {chat_history}
Context:{context}
Question:{question}

Answer:
"""
)

def format_docs(documents):
    """Format retrieved documents into a single text."""

    # Combine the retrieved chunks into one context
    return "\n".join(
        document.page_content for document in documents
    )

# Retrieve relevant document chunks
retriever = get_retriever()

rag_chain = (
    {
        "context": itemgetter("question") | retriever | format_docs,
        "question": itemgetter("question"),
        "chat_history": itemgetter("chat_history"),
    }
    | prompt
    | llm
    | StrOutputParser()
)

def ask_question(question: str, chat_history: str = ""):
    """Generate an answer using the RAG chain."""

    return rag_chain.invoke({
        "question": question,
        "chat_history": chat_history,
    })
