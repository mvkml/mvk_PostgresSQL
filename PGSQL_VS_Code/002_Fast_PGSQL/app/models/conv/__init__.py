"""Conversation models package - Pydantic DTOs for conversation-related data"""
from app.models.conv.ai_message_model import (
    AiMessageCreate,
    AiMessageResponse,
)

__all__ = [
    "AiMessageCreate",
    "AiMessageResponse",
]
