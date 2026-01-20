
from fastapi import Depends
from app.dal.connections.pgsql_connection import get_pgsql_db
from app.dal.connections.sql_connection import get_db
from app.dal.repositories.conv.ai_message_repo import AIMessageRepository
from app.dal.repositories.prompt_repository import PromptRepository
from app.dal.repositories.user_repository import UserRepository
from app.dal.utilities.module.map_user import MapUser
from sqlalchemy.orm.session import Session

def get_map_user() -> MapUser:
    return MapUser()

    
def get_user_repository(db = Depends(get_db), map_user = Depends(get_map_user)):
    user_repository = UserRepository(db, map_user)
    return user_repository


def di_get_prompt_repository(db = Depends(get_pgsql_db)):
    prompt_repository = PromptRepository(db)
    return prompt_repository


def di_get_ai_message_repo(db: Session = Depends(get_pgsql_db)):
    return AIMessageRepository(db)
    