from typing import TypedDict
from assistant.services.rag import rag_chain, llm
from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import ChatPromptTemplate

# Prompt for question classification
classification_prompt = ChatPromptTemplate.from_template("""
You are a classifier for a document-answering assistant.
Determine if the user's question is related to the content of the indexed documents.

Return "relevant" if the question concerns the documents.
Return "irrelevant" if the question does not concern the documents.

Question: {question}
""")

class GraphState(TypedDict):
    question: str
    context: str
    answer: str
    category: str

def generate_answer(state: GraphState):
    """Generate an answer using the RAG chain"""

    answer = rag_chain.invoke(state["question"])

    # Update state
    return {"answer": answer}

def classify_question(state: GraphState):
    """Classify a question"""

    messages = classification_prompt.format_messages(
        question=state["question"],
    )
    response = llm.invoke(messages)

    return {"category": response.content.strip()}

def irrelevant_question(state: GraphState):
    """Answer irrelevant questions"""

    return {"answer": "Your question is outside the scope of the indexed documents"}

def route_question(state: GraphState):
    """Route the question based on its category"""

    if state["category"].strip().lower() == "relevant":
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

def run(question: str):
    """Run the RAG"""
    result = graph.invoke({
        "question": question,
        "answer": "",
        "category": "",
    })


    return result["answer"]
