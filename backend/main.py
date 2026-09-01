"""
Sarvagya Backend - FastAPI application for AI trading chart analysis
"""
import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routes import chat, health

# Load environment variables from .env file (optional)
# Set SARVAGYA_SKIP_DOTENV=1 to skip loading .env (useful for diagnostics)
if os.getenv("SARVAGYA_SKIP_DOTENV") != "1":
    load_dotenv()
else:
    logger = logging.getLogger(__name__)
    logger.info("Skipping .env loading because SARVAGYA_SKIP_DOTENV=1")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle manager"""
    logger.info("Starting Sarvagya backend...")
    # Verify API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        logger.warning("GOOGLE_API_KEY environment variable not set - agent analysis will not work")
    else:
        logger.info("✓ GOOGLE_API_KEY configured")
    yield
    logger.info("Shutting down Sarvagya backend...")

app = FastAPI(
    title="Sarvagya",
    description="AI-powered trading chart analysis",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(chat.router)

@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "Sarvagya API", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn

    logger.info("Launching uvicorn on http://0.0.0.0:8000")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info",
    )

