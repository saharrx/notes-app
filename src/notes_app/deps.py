from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from notes_app.db import get_db
from notes_app.models import User
from notes_app.security import decode_access_token

DbSession = Annotated[Session, Depends(get_db)]

# Reads the "Authorization: Bearer <token>" header. tokenUrl tells /docs where to log in.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: DbSession) -> User:
    credentials_error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token", headers={"WWW-Authenticate": "Bearer"},)
    try:
        user_id = decode_access_token(token)
    except jwt.InvalidTokenError:
        raise credentials_error
    user = db.get(User, user_id)
    if user is None:
        raise credentials_error
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]