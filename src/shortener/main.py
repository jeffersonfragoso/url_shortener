import asyncio
import json


from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from bson import json_util
from starlette.datastructures import URL

from shortener.config import get_settings
from shortener import schemas
from shortener import mongodb
from shortener.mongodb import models


app = FastAPI()

loop = asyncio.get_event_loop()
producer = AIOKafkaProducer(
  loop=loop,
  bootstrap_servers="url_shortener-kafka-1:9092"
)

consumer_update_clicks = AIOKafkaConsumer(
  "update-clicks",
  bootstrap_servers="url_shortener-kafka-1:9092",
  loop=loop
)

async def consume():
  await consumer_update_clicks.start()
  try:
    async for msg in consumer_update_clicks:
      url_key = json.loads(msg.value)
      await mongodb.crud.update_db_clicks(url_key)
  finally:
    await consumer_update_clicks.stop()

@app.on_event("startup")
async def create_db_client():
  try:
    await mongodb.init_db()
    print("Successfully connected to the Mongo database.")

    await producer.start()
    loop.create_task(consume())

  except Exception as e:
    print(e)
    print("An error occurred while startup.")


async def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
  base_url = URL(get_settings().base_url)
  admin_endpoint = app.url_path_for(
    "administration info", secret_key=db_url.secret_key
  )

  admin_info = schemas.URLInfo(
    target_url=db_url.target_url,
    url=str(base_url.replace(path=db_url.key)),
    admin_url=str(base_url.replace(path=admin_endpoint)),
    clicks=db_url.clicks,
    is_active=db_url.is_active,
  )
  return admin_info


@app.get("/")
def read_root():
  return "Welcome to URL shortener API :)"


def raise_not_found(full_url):
  message = f"URL '{full_url}' doesn't exist"
  raise HTTPException(status_code=404, detail=message)


@app.post("/url")
async def create_url(url: schemas.URLBase):
  db_url = await mongodb.crud.create_db_url(url=url)
  result = await get_admin_info(db_url)
  return result

@app.get("/{url_key}")
async def forwad_to_target_url(
  url_key: str,
  request: Request,
):
  db_url = await mongodb.crud.get_db_url_by_key(url_key=url_key)
  if db_url:
    await producer.send(
      topic="update-clicks",
      value=json_util.dumps(db_url.key).encode("ascii")
    )
    return RedirectResponse(db_url.target_url)
  else:
    raise_not_found(str(request.url))


@app.get(
  "/admin/{secret_key}",
  name="administration info",
  response_model=schemas.URLInfo,
)
async def get_url_info(
  secret_key: str, request: Request
):
  if db_url := await mongodb.crud.get_db_url_by_secret_key(secret_key=secret_key):
    result = await get_admin_info(db_url)
    return result
  else:
    raise_not_found(request)


@app.delete("/admin/{secret_key}")
async def delete_url(
  secret_key: str,
  request: Request
):
  if db_url := await mongodb.crud.deactivate_db_url_by_secret_key(secret_key=secret_key):
    message = f'Succesfully deleted shortened URL for "{db_url.target_url}"'
    return {"detail": message}
  else:
    raise_not_found(request)
