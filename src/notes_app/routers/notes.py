from typing import Annotated
from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import select

from notes_app.deps import CurrentUser, DbSession
from notes_app.models import Note, User
from notes_app.schemas import NoteCreate, NoteOut, NoteUpdate

router = APIRouter(prefix="/notes", tags=["notes"])


def get_own_note(note_id: int, user: User, db: DbSession) -> Note:
    """Load a note that belongs to the user, or raise 404."""
    note = db.get(Note, note_id)
    # 404 (not 403) for other users' notes, so we don't reveal that the note exists.
    if note is None or note.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


@router.post("", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
def create_note(data: NoteCreate, current_user: CurrentUser, db: DbSession) -> Note:
    note = Note(**data.model_dump(), owner_id=current_user.id)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@router.get("", response_model=list[NoteOut])
def list_notes(
    current_user: CurrentUser,
    db: DbSession,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[Note]:
    query = (
        select(Note)
        .where(Note.owner_id == current_user.id)
        .order_by(Note.pinned.desc(), Note.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return list(db.scalars(query))


@router.get("/{note_id}", response_model=NoteOut)
def get_note(note_id: int, current_user: CurrentUser, db: DbSession) -> Note:
    return get_own_note(note_id, current_user, db)


@router.patch("/{note_id}", response_model=NoteOut)
def update_note(
    note_id: int, data: NoteUpdate, current_user: CurrentUser, db: DbSession
) -> Note:
    note = get_own_note(note_id, current_user, db)
    # Only the fields the client actually sent (and that aren't null).
    for field, value in data.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(note, field, value)
    db.commit()
    db.refresh(note)
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, current_user: CurrentUser, db: DbSession) -> None:
    note = get_own_note(note_id, current_user, db)
    db.delete(note)
    db.commit()