"""Local development entry point for the Sarvagya FastAPI application."""

from app import app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False, log_level="info")
