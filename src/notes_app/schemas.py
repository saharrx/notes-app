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


class Token(BaseModel):
    access_token:str
    token_type: str = "bearer"


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    pinned: bool = False


class NoteUpdate(BaseModel):
    """For PATCH: every field is optional, only the ones sent are changed."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    content: str | None = Field(default=None, min_length=1)
    pinned: bool | None = None


class NoteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    pinned: bool
    owner_id: int
    created_at: datetime
    updated_at: datetime
