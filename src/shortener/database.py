from sqlmodel import create_engine, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker

from .config import get_settings

engine = AsyncEngine(
  create_engine(
    url=get_settings().db_url,
    echo=True,
    future=True
  )
)

async def init_db():
  async with engine.begin() as conn:
    await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
  async_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False,
  )
  async with async_session() as session:
    yield session
