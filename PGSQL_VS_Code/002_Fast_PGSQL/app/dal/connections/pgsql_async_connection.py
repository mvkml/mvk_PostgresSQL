from typing import AsyncGenerator
from venv import create
from sqlalchemy import Text

from sqlalchemy.ext.asyncio import(
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)



DATABASE_URL="postgresql://postgres:Postgres%40007@localhost:5432/VikiHospitalBot"


engine = create_async_engine(DATABASE_URL,echo=False)
pgsql_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_pgsql_db_async()->AsyncGenerator[AsyncSession, None]:
    async with pgsql_session() as session:
        yield session


