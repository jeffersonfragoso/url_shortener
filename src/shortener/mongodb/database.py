from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from .models import URL

from shortener.config import get_settings

async def init_db():
  client = AsyncIOMotorClient(get_settings().db_url)
  await init_beanie(
    database=client.get_database(),
    document_models=[URL]
  )
