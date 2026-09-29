from fastapi import FastAPI
from pydantic import BaseModel

from agent import get_validated_response


app = FastAPI(
    title="Structured Output Clinic Chatbot",
    version="1.0.0"
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "message": "Structured Output Clinic Chatbot is running"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    response = get_validated_response(
        request.message
    )

    return response