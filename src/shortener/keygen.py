import secrets
import string
from shortener.mongodb import crud


async def create_random_key(length: int = 5) -> str:
  chars = string.ascii_uppercase + string.digits
  return "".join(secrets.choice(chars) for _ in range(length))


async def create_unique_random_key() -> str:
  key = await create_random_key()
  result = await crud.get_db_url_by_key(key)
  while result:
    key = await create_random_key()
  return key
