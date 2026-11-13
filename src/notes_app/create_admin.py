"""Make an existing user admin.
Usage: uv run python -m notes_app.create_admin<username>"""

import sys

from sqlalchemy import select

from notes_app.db import SessionLocal
from notes_app.models import User

def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("Usage: uv run python -m notes_app.create_admin <username>")
    username = sys.argv[1]
    with SessionLocal() as db:
        user = db.scalar(select(User).where(User.username == username))
        if user is None:
            sys.exit(f"No user named {username!r}. Register first.")
        user.role = "admin"
        db.commit()
    print(f"{username} is now an admin.")


if __name__ == "__main__":
    main()
