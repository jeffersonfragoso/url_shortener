from pydantic import BaseModel, AnyHttpUrl

class URLBase(BaseModel):
  target_url: AnyHttpUrl


class URL(URLBase):
  is_active: bool
  clicks: int

  class Config:
    orm_mode = True


class URLInfo(URL):
  url: str
  admin_url: str
