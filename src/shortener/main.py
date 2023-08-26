from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from starlette.datastructures import URL

from shortener.config import get_settings
from shortener import schemas
from shortener import mongodb
from shortener.mongodb import models


app = FastAPI()

@app.on_event("startup")
async def create_db_client():
    try:
        mongodb.init_db()
        print("Successfully connected to the Mongo database.")
    except Exception as e:
        print(e)
        print("An error occurred while connecting to Mongo database.")


def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
  base_url = URL(get_settings().base_url)
  admin_endpoint = app.url_path_for(
    "administration info", secret_key=db_url['secret_key']
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


def raise_not_found(request):
  message = f"URL '{request.url}' doesn't exist"
  raise HTTPException(status_code=404, detail=message)


@app.post("/url", response_model=schemas.URLInfo)
async def create_url(url: schemas.URLBase):
  db_url = mongodb.crud.create_db_url(url=url)
  result = get_admin_info(db_url)
  return result

@app.get("/{url_key}")
async def forwad_to_target_url(
  url_key: str,
  request: Request,
):
  db_url = mongodb.crud.get_db_url_by_key(url_key=url_key)
  if db_url:
    mongodb.crud.update_db_clicks(db_url=db_url)
    return RedirectResponse(db_url.target_url)
  else:
    raise_not_found(request)
    

@app.get(
  "/admin/{secret_key}",
  name="administration info",
  response_model=schemas.URLInfo,
)
async def get_url_info(
  secret_key: str, request: Request
):
  if db_url := mongodb.crud.get_db_url_by_secret_key(secret_key=secret_key):
    result = get_admin_info(db_url)
    return result
  else:
    raise_not_found(request)


@app.delete("/admin/{secret_key}")
async def delete_url(
  secret_key: str,
  request: Request
):
  if db_url := mongodb.crud.deactivate_db_url_by_secret_key(secret_key=secret_key):
    message = f'Succesfully deleted shortened URL for "{db_url.target_url}"'
    return {"detail": message}
  else:
    raise_not_found(request)
