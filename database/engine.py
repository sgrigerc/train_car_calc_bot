import os
from dotenv import dotenv_values, load_dotenv, find_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from database.models import Base

load_dotenv(find_dotenv())
DB_LITE = 'sqlite+aiosqlite:///my_base.db'


engine = create_async_engine(DB_LITE, echo=False)   #эхо выводит значения в терминал

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_db():
   async with engine.begin() as conn:
      await conn.run_sync(Base.metadata.create_all)


async def drop_db():
   async with engine.begin() as conn:
      await conn.run_sync(Base.metadata.drop_all)




