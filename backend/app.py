import os
import logging
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import chat, health
from services.agent_adapter import AgentAdapter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_ai() -> AgentAdapter:
    """Initialize the AI client for the application."""
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.warning("GOOGLE_API_KEY not set - chart analysis will not work")
    return AgentAdapter()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Sarvagya backend...")
    app.state.ai = init_ai()
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if api_key:
        logger.info("✓ GOOGLE_API_KEY configured")
    yield
    logger.info("Shutting down Sarvagya backend...")


def create_app() -> FastAPI:
    if os.getenv("SARVAGYA_SKIP_DOTENV") != "1":
        load_dotenv()

    app = FastAPI(
        title="Sarvagya",
        description="AI-powered trading chart analysis",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.state.ai = init_ai()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(chat.router)

    @app.get("/")
    def root():
        return {"message": "Sarvagya API", "version": "1.0.0"}

    return app


app = create_app()
