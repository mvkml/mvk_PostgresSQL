
from sqlalchemy.orm.session import Session
from app.dal.repositories.sql_base_repository import SQLBaseRepository

class PromptRepository():
    def __init__(self,db:Session):
        self.db = db
        pass