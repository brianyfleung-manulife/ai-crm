from fastapi import APIRouter
from utils.graph import graph
from pydantic import BaseModel


router = APIRouter(prefix="/chatbot", tags=["chatbot"])

class ChatInput(BaseModel):
    messages: list[str]
    thread_id: str

@router.post("/")
async def get_response(input: ChatInput):
    config = {"configurable": {"thread_id": input.thread_id}}
    response = await graph.ainvoke({"messages": input.messages}, config=config)
    return {"response": response["messages"][-1].content}
