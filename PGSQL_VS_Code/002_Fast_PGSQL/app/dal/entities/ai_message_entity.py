from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy import Integer,String,Text,CheckConstraint,DateTime,func
from sqlalchemy.dialects.postgresql import UUID,JSONB
from app.dal.entities.base_entity import Base
import uuid
from datetime import datetime


class AIMessageEntity(Base):
    __tablename__ = "ai_message"
    __table_args__ = (
        CheckConstraint(
            "role IN ('system','user','assistant','tool')",
            name="ai_message_role_check"
        ),{"schema": "conv"}
    )

    message_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),  # DB default
    )

    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)

    tenant_id: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[str] = mapped_column(Text, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    meta: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        server_default="{}"  # DB default jsonb
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    
    '''
    -- Table: conv.ai_message

-- DROP TABLE IF EXISTS conv.ai_message;

CREATE TABLE IF NOT EXISTS conv.ai_message
(
    message_id uuid NOT NULL DEFAULT gen_random_uuid(),
    session_id uuid NOT NULL,
    tenant_id text COLLATE pg_catalog."default" NOT NULL,
    user_id text COLLATE pg_catalog."default" NOT NULL,
    role text COLLATE pg_catalog."default" NOT NULL,
    content text COLLATE pg_catalog."default" NOT NULL,
    meta jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT ai_message_pkey PRIMARY KEY (message_id),
    CONSTRAINT ai_message_role_check CHECK (role = ANY (ARRAY['system'::text, 'user'::text, 'assistant'::text, 'tool'::text]))
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS conv.ai_message
    OWNER to postgres;
    
    '''



