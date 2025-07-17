
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Add CORS middleware to allow React frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    message: str

# Step 1: Get the auth token from Azure AD
def get_azure_ad_token():
    tenant_id = os.getenv("AZURE_TENANT_ID")
    client_id = os.getenv("AZURE_CLIENT_ID")
    client_secret = os.getenv("AZURE_CLIENT_SECRET")
    scope = os.getenv("AZURE_SCOPE")
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "scope": scope,
        "client_secret": client_secret
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

# Initialize the Azure OpenAI client
def initialize_chat_client():
    token = get_azure_ad_token()
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview")
    subscription_key = os.getenv("AZURE_SUBSCRIPTION_KEY")

    custom_headers = {
        "Authorization": f"Bearer {token}",
        "Ocp-Apim-Subscription-Key": subscription_key
    }

    chat = AzureChatOpenAI(
        azure_endpoint=azure_endpoint,
        azure_deployment=deployment_name,
        api_version=api_version,
        openai_api_key="dummy-key",
        default_headers=custom_headers
    )
    return chat

def process_message(message: str) -> str:
    """Process the user message and get a response from Azure OpenAI."""
    try:
        chat = initialize_chat_client()
        messages = [HumanMessage(content=message)]
        response = chat.invoke(messages)
        return response.content
    except Exception as e:
        return f"Error processing message: {str(e)}"

@app.get("/")
async def root():
    return {"message": "AI CRM Chatbot API is running!"}

@app.post("/chatbot/")
async def get_response(query: Query):
    response = process_message(query.message)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
