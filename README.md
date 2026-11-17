# Notes API

A REST API for personal notes, built with FastAPI and PostgreSQL. Users register, log in with a
JWT, and manage their own notes. Admins can manage users and see every note.

## Features

- **Auth:** registration, login with JWT access tokens, and passwords hashed with Argon2
- **Notes:** create, list, read, update and delete your own notes. Other users' notes are not visible to you.
- **Pagination:** `limit`/`offset` on the list endpoint. Pinned notes come first, then the newest.
- **Roles:** `user` and `admin`. Admin endpoints are under `/admin`.
- **Migrations:** the database schema is versioned with Alembic.

## Tech stack

Python 3.12 · FastAPI · SQLAlchemy 2 · PostgreSQL 18 · Alembic · PyJWT · pwdlib (Argon2) ·
pydantic-settings · Docker Compose · uv

## Getting started

You need [uv](https://docs.astral.sh/uv/) and Docker.

```bash
# 1. Configuration: copy the template and set your own JWT_SECRET_KEY
cp .env.example .env

# 2. Start PostgreSQL in Docker
docker compose up -d

# 3. Install dependencies and create the database tables
uv sync
uv run alembic upgrade head

# 4. Run the API with auto-reload
uv run uvicorn notes_app.main:app --reload
```

The interactive API docs are then at <http://localhost:8000/docs>.

To make a registered user an admin:

```bash
uv run python -m notes_app.create_admin <username>
```

## Endpoints

| Method | Path | Who | Description |
|---|---|---|---|
| POST | `/auth/register` | anyone | Create an account |
| POST | `/auth/login` | anyone | Get a JWT access token |
| GET | `/auth/me` | logged in | Current user |
| POST | `/notes` | logged in | Create a note |
| GET | `/notes?limit=&offset=` | logged in | List your notes |
| GET | `/notes/{id}` | owner | Read a note |
| PATCH | `/notes/{id}` | owner | Update a note |
| DELETE | `/notes/{id}` | owner | Delete a note |
| GET | `/admin/users` | admin | List all users |
| GET | `/admin/notes` | admin | List all notes |
| PATCH | `/admin/users/{id}/role` | admin | Change a user's role |
| DELETE | `/admin/users/{id}` | admin | Delete a user |

## Project structure

```
src/notes_app/
  main.py          FastAPI app, includes the routers
  config.py        settings from environment / .env
  db.py            SQLAlchemy engine and session
  models.py        User and Note tables
  schemas.py       Pydantic request/response models
  security.py      password hashing and JWT creation/verification
  deps.py          shared dependencies (DB session, current user, admin check)
  routers/         auth, notes and admin endpoints
  create_admin.py  promote a user to admin
migrations/        Alembic migration scripts
```

## Roadmap

- [ ] Tests with pytest
- [ ] Dockerfile for the API itself
- [ ] CI with GitHub Actions
