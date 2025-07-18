from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter(prefix="/chatbot", tags=["chatbot"])

class Query(BaseModel):
    message: str

@router.post("/")
async def get_response(query: Query):
    # Simple LangChain chat logic (replace with your LangChain call as needed)
    from utils.openai_message import process_message
    response = process_message(query.message)
    return {"response": response}
