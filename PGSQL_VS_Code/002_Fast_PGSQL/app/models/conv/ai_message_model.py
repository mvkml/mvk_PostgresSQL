from datetime import datetime
from typing import Any, Dict, Literal, Optional
from urllib import response
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.common.common_base import ItemBase, ModelBase

# Allowed roles (same as DB constraint)
AiRole = Literal["system", "user", "assistant", "tool"]

class AiMessageCreate(BaseModel):
    session_id: UUID
    tenant_id: str
    user_id: str
    role: AiRole
    content: str
    meta: Dict[str, Any] = Field(default_factory=dict)

class AiMessageRequest(BaseModel):
    message_id: UUID
    session_id: UUID
    tenant_id: str
    user_id: str
    role: AiRole
    content: str
    meta: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True  # SQLAlchemy → Pydantic

class AiMessageResponse(BaseModel):
    message_id: UUID
    session_id: UUID
    tenant_id: str
    user_id: str
    role: AiRole
    content: str
    meta: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True  # SQLAlchemy → Pydantic

class AIMessageItem(ItemBase):
    message_id: UUID
    session_id: UUID
    tenant_id: str
    user_id: str
    role: AiRole
    content: str
    meta: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True  # SQLAlchemy → Pydantic
 
class AIMessageModel(ModelBase):
    request: Optional[AiMessageRequest] = None
    response: Optional[AiMessageResponse] = None # is this correct ?
    item: Optional[AIMessageItem] = None # is this correct ?



