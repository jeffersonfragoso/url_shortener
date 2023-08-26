from sqlmodel import Session
from sqlmodel import select
from . import keygen, models, schemas


async def create_db_url(session: Session, url: schemas.URLBase) -> models.URL:

    key = await keygen.create_unique_random_key(session)
    adm_key = await keygen.create_random_key(8)
    secret_key = f"{key}_{adm_key}"

    db_url = models.URL(
        target_url=url.target_url, key=key, secret_key=secret_key
    )
    session.add(db_url)
    await session.commit()
    await session.refresh(db_url)
    return db_url

async def get_db_url_by_key(session: Session, url_key: str) -> models.URL:
  result = await session.execute(
    select(models.URL) \
      .where(models.URL.key == url_key, models.URL.is_active)
  )
  return result.scalars().one_or_none()

async def get_db_url_by_secret_key(session: Session, secret_key: str) -> models.URL:
  result = await session.execute(
    select(models.URL) \
      .where(models.URL.secret_key == secret_key, models.URL.is_active)
  )
  return result.scalars().one_or_none()

async def update_db_clicks(session: Session, db_url: models.URL) -> models.URL:
  db_url.clicks += 1
  await session.commit()
  await session.refresh(db_url)
  return db_url

async def deactivate_db_url_by_secret_key(session: Session, secret_key: str) -> models.URL:
  db_url = await get_db_url_by_secret_key(session, secret_key)
  print(db_url)
  if db_url:
    db_url.is_active = False
    await session.commit()
    await session.refresh(db_url)

  return db_url
