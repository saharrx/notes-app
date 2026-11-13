from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import select

from notes_app.deps import AdminUser, DbSession
from notes_app.models import User, Note
from notes_app.schemas import RoleUpdate, UserOut, NoteOut

router = APIRouter(prefix="/admin", tags=["admin"])


def get_user_or_404(user_id: int, db: DbSession) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    return user


@router.get("/users", response_model=list[UserOut])
def list_users(
    admin: AdminUser,
    db: DbSession,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    ) -> list[User]:
    query = select(User).order_by(User.id).limit(limit).offset(offset)
    return list(db.scalars(query))


@router.get("/notes", response_model=list[NoteOut])
def list_all_notes(
    admin: AdminUser,
    db: DbSession,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    ) -> list[Note]:
    query = select(Note).order_by(Note.created_at.desc()).limit(limit).offset(offset)
    return list(db.scalars(query))


@router.patch("/users/{user_id}/role", response_model=UserOut)
def change_role(user_id: int, data:RoleUpdate, admin: AdminUser, db: DbSession) -> User:
    if user_id == admin.id:
        #stops the last admin from accedentally locking everyone out
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="you can't change your own role")
    user = get_user_or_404(user_id, db)
    user.role = data.role
    db.commit()
    db.refresh(user)
    return user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, admin: AdminUser, db: DbSession) -> None:
    if user_id == admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="You can't delete yourself"
        )
    user = get_user_or_404(user_id, db)
    db.delete(user)  # their notes are deleted too (cascade)
    db.commit()