import os
import requests
from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

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

    llm = AzureChatOpenAI(
        azure_endpoint=azure_endpoint,
        azure_deployment=deployment_name,
        api_version=api_version,
        openai_api_key="dummy-key",
        default_headers=custom_headers
    )

    prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "{system_message}"),
        MessagesPlaceholder("messages")
    ]
)

    chat = prompt_template | llm

    return chat
