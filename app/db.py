import asyncio

import sqlalchemy as db
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

DB_NAME = 'teamapp'  # TODO: move to .env


class UserTable(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Database:
    def __init__(self, name):
        self.name = name
        self._init_engine()
        self._init_session()
        self._init_metadata()

    def _init_engine(self):
        self.engine = create_async_engine(f'sqlite+aiosqlite:///{self.name}.sqlite', echo=True,)

    def _init_session(self):
        self.session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

    def _init_metadata(self):
        self.metadata = db.MetaData()

    async def create_database(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


async def async_main():
    await Database(DB_NAME).create_database()

if __name__ == '__main__':
    asyncio.run(async_main())
