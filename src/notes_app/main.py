from fastapi import FastAPI

from notes_app.config import get_settings

settings = get_settings()

app = FastAPI(title=settings.app_name, version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness check: Docker and CI use this to see if the API is up."""
    return {"status": "ok", "environment": settings.environment}

@app.get("/hello/{name}")
def hello(name: str, shout: bool = False) -> dict[str, str]:
    message =f"Hello, {name}!"
    if shout:
        message = message.upper()
    return {"message": message}