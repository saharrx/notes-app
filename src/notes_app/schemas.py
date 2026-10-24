from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    """What the client sends to register."""

    username: str = Field(min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$")
    password: str = Field(min_length=8, max_length=128)


class UserOut(BaseModel):
    """What the API sends back about a user. No password hash:D"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    role: str
    created_at: datetime