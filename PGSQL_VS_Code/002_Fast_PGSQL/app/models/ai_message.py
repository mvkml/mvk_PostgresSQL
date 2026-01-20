import datetime
import uuid

from sqlalchemy import CheckConstraint, DateTime, PrimaryKeyConstraint, Text, Uuid, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


class AiMessage(Base):
    __tablename__ = 'ai_message'
    __table_args__ = (
        CheckConstraint("role = ANY (ARRAY['system'::text, 'user'::text, 'assistant'::text, 'tool'::text])", name='ai_message_role_check'),
        PrimaryKeyConstraint('message_id', name='ai_message_pkey'),
        {'schema': 'conv'}
    )

    message_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    session_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    tenant_id: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[str] = mapped_column(Text, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    meta: Mapped[dict] = mapped_column(JSONB, nullable=False, server_default=text("'{}'::jsonb"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
