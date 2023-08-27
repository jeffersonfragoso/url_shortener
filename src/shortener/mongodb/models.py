from beanie import Document
from pydantic import Field


class URL(Document):

    key: str = Field(unique=True, index=True)
    secret_key: str = Field(unique=True, index=True)
    target_url: str = Field(index=True)
    is_active: bool = Field(default=True)
    clicks: int = Field(default=0)

    class Settings:
        name = "urls"
        use_state_management = True
