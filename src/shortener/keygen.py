import secrets
import string
from sqlmodel import Session
from . import crud


async def create_random_key(length: int = 5) -> str:
  chars = string.ascii_uppercase + string.digits
  return "".join(secrets.choice(chars) for _ in range(length))


async def create_unique_random_key(session: Session) -> str:
  key = await create_random_key()
  result = await crud.get_db_url_by_key(session, key)
  while result:
    key = await create_random_key()
  return key
