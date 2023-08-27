from shortener import keygen, schemas

from shortener.mongodb import models

async def create_db_url(url: schemas.URLBase) -> models.URL:

    key = await keygen.create_unique_random_key()
    adm_key = await keygen.create_random_key(8)
    secret_key = f"{key}_{adm_key}"

    db_url = models.URL(
      target_url=url.target_url,
      key=key,
      secret_key=secret_key
    )

    await db_url.insert()
    return db_url

async def get_db_url_by_key(url_key: str) -> models.URL:
  try:
    return await models.URL.find_one(
      models.URL.key==url_key,
      models.URL.is_active==True
    )
  except Exception as e:
    return None

async def get_db_url_by_secret_key(secret_key: str) -> models.URL:
  try:
    return await models.URL.find_one(
      models.URL.secret_key==secret_key,
      models.URL.is_active==True
    )
  except Exception as e:
    return None

async def update_db_clicks(db_url: models.URL) -> models.URL:
  db_url.clicks += 1
  await db_url.save_changes()
  return db_url

async def deactivate_db_url_by_secret_key(secret_key: str) -> models.URL:
  db_url = await get_db_url_by_secret_key(secret_key)
  if db_url:
    db_url.is_active = False
    await db_url.save_changes()

  return db_url
