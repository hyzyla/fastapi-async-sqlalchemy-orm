from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app import session_scope

engine = create_async_engine("sqlite+aiosqlite:///db.sqlite3", echo=True, future=True)
AsyncSessionFactory = sessionmaker(bind=engine, class_=AsyncSession)

# Function `get_session_context` controls when to create a new session.
# In our case, a new session context will be created for every request,
# so calling session methods inside the HTTP handlers will create one
# session per request.
session = async_scoped_session(
    session_factory=AsyncSessionFactory,
    scopefunc=session_scope.get_session_context,
)
Base = declarative_base(bind=engine)


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    session_id = Column(Text)
    request_id = Column(Text)


async def create_all_tables():
    """create all tables in database"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
