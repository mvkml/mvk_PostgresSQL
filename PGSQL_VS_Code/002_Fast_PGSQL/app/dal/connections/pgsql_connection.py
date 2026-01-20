from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker,Session

DATABASE_URL="postgresql://postgres:Postgres%40007@localhost:5432/VikiHospitalBot"

bind_engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True # about this ? 
)

pg_sql_session = sessionmaker(bind=bind_engine,autoflush=False)


# return type Session ( sqlalchemy.orm.session.Session)
def get_pgsql_db():
    db = pg_sql_session()
    try:
        yield db
    finally:
        db.close()

