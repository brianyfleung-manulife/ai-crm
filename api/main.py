# Utility: Extract customer filter parameters from a chat message using the LLM
def extract_customer_filters_from_message(message: str) -> dict:
    """
    Use the LLM to extract customer filter parameters from a user message.
    Returns a dict of filter params, e.g. {"gender": "female", "riskProfile": "high", "aum_min": 100000}
    """
    chat = initialize_chat_client()
    system_prompt = (
        "You are an assistant that extracts filter parameters for a customer table. "
        "Given a user message, return a JSON object with any of these fields if present: "
        "gender, riskProfile, aum_min, aum_max, age_min, age_max, search, sort_by, sort_dir. "
        "If a field is not mentioned, omit it. Only return the JSON object."
    )
    prompt = f"{system_prompt}\nUser message: {message}\nJSON:"
    messages = [HumanMessage(content=prompt)]
    response = chat.invoke(messages)
    import json
    try:
        # Find the first JSON object in the response
        import re
        match = re.search(r'{.*}', response.content, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        else:
            return {}
    except Exception:
        return {}

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv
from routers import customers


# Load environment variables from .env file
load_dotenv()



# Create a sub-app for API and mount it under /api
api_app = FastAPI()
api_app.include_router(customers.router)

app = FastAPI()
# Add CORS middleware to allow React frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the API app under /api
app.mount("/api", api_app)

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



# Import the filter_customers function from the customers router
from routers.customers import filter_customers

@api_app.post("/chatbot/")
async def get_response(query: Query):
    # Step 1: Try to extract filter params from the message
    filters = extract_customer_filters_from_message(query.message)
    if filters:
        # Only pass allowed filter keys
        allowed_keys = {"search", "sort_by", "sort_dir", "gender", "riskProfile", "aum_min", "aum_max", "age_min", "age_max"}
        filter_args = {k: v for k, v in filters.items() if k in allowed_keys}
        # Call the filter_customers function directly
        customers_result = filter_customers(**filter_args)
        # Format as a simple table string (showing key fields)
        if customers_result:
            table = "ID | Name | Age | Gender | Risk | AUM | LastContact\n"
            table += "-" * 65 + "\n"
            for c in customers_result:
                table += f"{c['id']} | {c['name']} | {c['age']} | {c['gender']} | {c['riskProfile']} | {c['aum']} | {c['lastContact']}\n"
            return {"response": table, "customers": customers_result}
        else:
            return {"response": "No customers found matching your criteria.", "customers": []}
    # Fallback: normal chat
    response = process_message(query.message)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
