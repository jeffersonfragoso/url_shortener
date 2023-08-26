from shortener import keygen, schemas
from mongoengine.errors import DoesNotExist

from shortener.mongodb import models

def create_db_url(url: schemas.URLBase) -> models.URL:

    key = keygen.create_unique_random_key()
    adm_key = keygen.create_random_key(8)
    secret_key = f"{key}_{adm_key}"

    db_url = models.URL(
        target_url=url.target_url, key=key, secret_key=secret_key
    )

    db_url.save()
    return db_url

def get_db_url_by_key(url_key: str) -> models.URL:
  try:
    return models.URL.objects.get(key=url_key, is_active=True)
  except DoesNotExist as e:
    return None

def get_db_url_by_secret_key(secret_key: str) -> models.URL:
  try:
    return models.URL.objects.get(secret_key=secret_key, is_active=True)
  except DoesNotExist as e:
    return None

def update_db_clicks(db_url: models.URL) -> models.URL:
  db_url.update(inc__clicks = 1)
  return db_url

def deactivate_db_url_by_secret_key(secret_key: str) -> models.URL:
  db_url = get_db_url_by_secret_key(secret_key)
  if db_url:
    db_url.update(is_active=False)

  return db_url
