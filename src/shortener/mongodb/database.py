from mongoengine import connect

from shortener.config import get_settings

def init_db():
  connect(host=get_settings().db_url)
