from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from notes_app.deps import DbSession
from notes_app.models import User
from notes_app.schemas import UserCreate, UserOut
from notes_app.security import hash_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: DbSession) -> User:
    user = User(username=data.username, password_hash=hash_password(data.password))
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        # The UNIQUE constraint on username rejected the insert.
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already taken")
    db.refresh(user)  # load id, role, created_at that the database filled in
    return user