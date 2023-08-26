import secrets
import string
from shortener.mongodb import crud


def create_random_key(length: int = 5) -> str:
  chars = string.ascii_uppercase + string.digits
  return "".join(secrets.choice(chars) for _ in range(length))


def create_unique_random_key() -> str:
  key = create_random_key()
  result = crud.get_db_url_by_key(key)
  while result:
    key = create_random_key()
  return key
