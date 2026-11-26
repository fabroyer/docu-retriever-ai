from typing import TypedDict
from assistant.services.rag import rag_chain, llm
from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import ChatPromptTemplate

# Prompt for question classification
classification_prompt = ChatPromptTemplate.from_template("""
You are a classifier for a document-answering assistant.
Determine if the user's question is related to the content of the indexed documents.

Return "document" if the question concerns the documents.
return "conversation" if the question concerns the previous messages.
Return "irrelevant" if the question does not concern the documents.

Question: {question}
Conversation history: {chat_history}

Return only one category : document, conversation or irrelevant.
""")

class GraphState(TypedDict):
    question: str
    chat_history: str
    answer: str
    category: str

def generate_answer(state: GraphState):
    """Generate an answer using the RAG chain"""

    answer = rag_chain.invoke({
        "question": state["question"],
        "chat_history": state["chat_history"],
    })

    # Update state
    return {"answer": answer}

def classify_question(state: GraphState):
    """Classify a question"""

    messages = classification_prompt.format_messages(
        question=state["question"],
        chat_history=state["chat_history"],
    )
    response = llm.invoke(messages)

    return {"category": response.content.strip()}

def irrelevant_question(state: GraphState):
    """Answer irrelevant questions"""

    return {"answer": "Your question is outside the scope of the indexed documents"}

def route_question(state: GraphState):
    """Route the question based on its category"""

    if state["category"].strip().lower() == "document":
        return "generate_answer"

    if state["category"].strip().lower() == "conversation":
        return "generate_answer"

    return "irrelevant_question"

# Creta graph
graph = StateGraph(GraphState)

# Nodes
graph.add_node("classify_question", classify_question)
graph.add_node("generate_answer", generate_answer)
graph.add_node("irrelevant_question", irrelevant_question)

# Edges
graph.add_edge(START, "classify_question")
graph.add_conditional_edges(
    "classify_question",
    route_question,
    {"generate_answer": "generate_answer",
     "irrelevant_question": "irrelevant_question",}
)
graph.add_edge("generate_answer", END)
graph.add_edge("irrelevant_question", END)

# Compile
graph = graph.compile()

# None if the question require memory.
def run(question: str, chat_history: list = None):
    """Run the RAG"""

    # None to prevent an error for the next step.
    if chat_history is None:
        chat_history = []

    history = "\n".join(chat_history)

    result = graph.invoke({
        "question": question,
        "chat_history": history,
        "answer": "",
        "category": "",
    })


    return result["answer"]
