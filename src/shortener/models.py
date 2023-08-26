from sqlmodel import SQLModel, Field

class URL(SQLModel, table=True):
  __tablename__ = "urls"

  id: int = Field(default=None, nullable=False, primary_key=True)
  key: str = Field(unique=True, index=True)
  secret_key: str = Field(unique=True, index=True)
  target_url:str = Field(index=True)
  is_active: bool = Field(default=True)
  clicks: int = Field(default=0)
