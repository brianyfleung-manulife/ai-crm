from utils.openai_client import initialize_chat_client
from langchain.schema import HumanMessage

def process_message(message: str) -> str:
    """Process the user message and get a response from Azure OpenAI."""
    try:
        chat = initialize_chat_client()
        messages = [HumanMessage(content=message)]
        response = chat.invoke(messages)
        return response.content
    except Exception as e:
        return f"Error processing message: {str(e)}"
