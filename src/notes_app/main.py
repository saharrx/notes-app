from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from notes_app.config import get_settings
from notes_app.db import get_db
from notes_app.config import get_settings

settings = get_settings()

app = FastAPI(title=settings.app_name, version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness check: Docker and CI use this to see if the API is up. """
    return {"status": "ok", "environment": settings.environment}

@app.get("/health/db")
def health_db(db: Annotated[Session, Depends(get_db)]) -> dict[str, str]:
    """Check that the API can reach Postgres."""
    db.execute(text("SELECT 1"))
    return {"database": "ok"}
#Depends(get_db) is dependency injection

@app.get("/hello/{name}")
def hello(name: str, shout: bool = False) -> dict[str, str]:
    message =f"Hello, {name}!"
    if shout:
        message = message.upper()
    return {"message": message}