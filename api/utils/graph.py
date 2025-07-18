from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

from utils.openai_client import initialize_chat_client

class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: State):
    print('statrt chatbot')
    # Invoke LLM Model
    chat = initialize_chat_client()
    system_message = "You are a helpful assistant. You are a human being. Talk like a human."
    response = chat.invoke({"system_message": system_message, "messages": state["messages"]})
    return {"messages": [response]}

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile(checkpointer=MemorySaver())