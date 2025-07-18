from utils.openai_client import initialize_chat_client
from langchain.schema import HumanMessage

from langchain.schema import AIMessage

# Simple in-memory chat history (for demo only; replace with persistent storage for production)
chat_history = []

def process_message(message: str) -> str:
    """Process the user message and get a response from Azure OpenAI, persisting chat history."""
    try:
        chat = initialize_chat_client()
        # Add the new user message to the history
        chat_history.append(HumanMessage(content=message))
        # Get response from the model using the full history
        response = chat.invoke(chat_history)
        # Add the AI response to the history
        chat_history.append(AIMessage(content=response.content))
        return response.content
    except Exception as e:
        return f"Error processing message: {str(e)}"
