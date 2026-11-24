"""
RAG service.
Generates answers based on retrieved documents chunks.
"""
from typing import cast

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from assistant.services.retrieval import get_retriever

# Initialize the language model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Create the prompt
prompt = ChatPromptTemplate.from_template("""
Answer the question using only the following context.
If the answer is not in the context, say that you don't know.

Context:{context}
Question:{question}
"""
)

def ask_question(question):
    """Generates answers based on retrieved documents chunks."""

    # Retrieve relevant document chunks
    retriever = get_retriever()
    documents = retriever.invoke(question)

    # Combine the retrieved chunks into one context
    context = "\n".join(
        document.page_content for document in documents
    )

    # Create the prompt with the context and question
    messages = prompt.format_messages(
        context=context,
        question=question,
    )

    # Generate tje answer
    response = llm.invoke(messages)

    return response.content