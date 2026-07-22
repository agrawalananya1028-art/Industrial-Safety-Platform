"""Chat/Chatbot API Routes"""

from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.agents.chatbot import chatbot_agent
from app.services import chat as chat_service

router = APIRouter()


class ChatMessage(BaseModel):
    user_id: UUID
    message: str
    context: dict = {}


class ChatResponse(BaseModel):
    message: str
    context: dict
    sources: List[str]
    follow_up_questions: List[str]


@router.post("/message", response_model=ChatResponse)
async def send_chat_message(chat_input: ChatMessage, db: Session = Depends(get_db)) -> ChatResponse:
    """Send message to AI safety chatbot"""
    response = await chatbot_agent.process_query(db, chat_input.message, chat_input.context)
    return response


@router.get("/history/{user_id}")
async def get_chat_history(user_id: UUID, db: Session = Depends(get_db), limit: int = 50) -> List[dict]:
    """Get chat history for user"""
    history = await chat_service.get_history(db, user_id, limit)
    return history


@router.get("/explain-alert/{alert_id}")
async def explain_alert(alert_id: UUID, db: Session = Depends(get_db)):
    """Get AI explanation for an alert"""
    explanation = await chatbot_agent.explain_alert(db, alert_id)
    if not explanation:
        raise HTTPException(status_code=404, detail="Alert not found")
    return explanation


@router.get("/suggest-actions/{risk_zone}")
async def suggest_actions(risk_zone: str, db: Session = Depends(get_db)):
    """Get AI suggested actions for a risk zone"""
    actions = await chatbot_agent.suggest_actions(db, risk_zone)
    return actions
