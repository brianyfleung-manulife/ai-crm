
# Utility import for extracting customer filter parameters
from utils.customer_filters import extract_customer_filters_from_message

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv
from routers import customers
from routers import chatbot
import certifi

# Set certificate bundle path
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
os.environ['SSL_CERT_FILE'] = certifi.where()

# Load environment variables from .env file
load_dotenv()




# Create a sub-app for API and mount it under /api
api_app = FastAPI()
api_app.include_router(customers.router)
api_app.include_router(chatbot.router)

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

# OpenAI client utility
from utils.openai_client import initialize_chat_client
# Message processing utility
from utils.openai_message import process_message

@app.get("/")
async def root():
    return {"message": "AI CRM Chatbot API is running!"}





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
