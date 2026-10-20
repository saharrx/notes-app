from collections.abc import Iterator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from notes_app.config import get_settings

engine = create_engine(get_settings().database_url)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    """parent class of all tables"""


def get_db() -> Iterator[Session]:
    #one session per request
    with SessionLocal() as session:
        yield session