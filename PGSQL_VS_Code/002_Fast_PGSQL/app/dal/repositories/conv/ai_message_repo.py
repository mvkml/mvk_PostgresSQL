from app.dal.repositories.base_repository import BaseRepository
from sqlalchemy.orm import session

class AIMessageRepository(BaseRepository):
      def __init__(self,db:session):
            super().__init__()
            self.db = db
            


            
