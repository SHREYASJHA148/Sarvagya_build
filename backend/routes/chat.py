"""
Chat and analysis endpoints
"""
import logging
import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid

from services.agent_adapter import AgentAdapter
from schemas.chat import ChatRequest, ChatResponse, ErrorResponse

router = APIRouter(prefix="/api", tags=["chat"])
logger = logging.getLogger(__name__)

# Initialize agent adapter
agent = AgentAdapter()

class ConversationManager:
    """Simple in-memory conversation manager for the hackathon"""
    def __init__(self):
        self.conversations = {}

    def create_conversation(self):
        """Create a new conversation"""
        conv_id = str(uuid.uuid4())
        self.conversations[conv_id] = {
            "messages": [],
            "created_at": None,
            "last_message_at": None
        }
        return conv_id

    def add_message(self, conv_id: str, role: str, content: str, image_path: Optional[str] = None):
        """Add a message to conversation"""
        if conv_id not in self.conversations:
            raise ValueError(f"Conversation {conv_id} not found")

        self.conversations[conv_id]["messages"].append({
            "role": role,
            "content": content,
            "image_path": image_path
        })

    def get_conversation(self, conv_id: str):
        """Get conversation messages"""
        return self.conversations.get(conv_id, {}).get("messages", [])

conversation_manager = ConversationManager()

@router.post("/chat")
async def chat_endpoint(
    message: str = Form(...),
    conversation_id: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
) -> ChatResponse:
    """
    Process a chat message with optional image attachment

    Args:
        message: User's text message
        conversation_id: Optional existing conversation ID
        file: Optional chart image file

    Returns:
        ChatResponse with analysis or error
    """
    request_id = str(uuid.uuid4())

    try:
        # Validate input
        if not message or not message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        message = message.strip()

        # Create or use existing conversation
        if not conversation_id:
            conversation_id = conversation_manager.create_conversation()

        # Handle file upload
        image_path = None
        if file:
            if not _validate_file(file):
                raise HTTPException(status_code=400, detail="Invalid file type or size")

            image_path = await _save_upload(file, conversation_id, request_id)

        # Add user message to conversation
        conversation_manager.add_message(conversation_id, "user", message, image_path)

        # Get conversation history for context
        history = conversation_manager.get_conversation(conversation_id)

        # Invoke agent
        logger.info(f"[{request_id}] Invoking agent with message: {message[:100]}...")
        response = agent.analyze(
            message=message,
            image_path=image_path,
            conversation_history=history,
            request_id=request_id
        )

        # Add assistant response to conversation
        conversation_manager.add_message(conversation_id, "assistant", response)

        logger.info(f"[{request_id}] Analysis complete")

        return ChatResponse(
            message=response,
            conversation_id=conversation_id,
            request_id=request_id
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[{request_id}] Error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An error occurred during analysis. Please try again."
        )

def _validate_file(file: UploadFile) -> bool:
    """Validate uploaded file"""
    ALLOWED_TYPES = {"image/png", "image/jpeg", "image/webp"}

    if file.content_type not in ALLOWED_TYPES:
        return False

    return True

async def _save_upload(file: UploadFile, conv_id: str, request_id: str) -> str:
    """Save uploaded file temporarily"""
    import tempfile
    import shutil

    # Create temp directory for uploads
    upload_dir = "/tmp/sarvagya_uploads"
    os.makedirs(upload_dir, exist_ok=True)

    # Save file
    file_ext = os.path.splitext(file.filename)[1]
    temp_path = os.path.join(upload_dir, f"{request_id}{file_ext}")

    try:
        contents = await file.read()

        # Check actual file size
        MAX_SIZE = 10 * 1024 * 1024
        if len(contents) > MAX_SIZE:
            raise HTTPException(status_code=413, detail="File too large")

        with open(temp_path, "wb") as f:
            f.write(contents)

        logger.info(f"[{request_id}] Saved upload: {temp_path}")
        return temp_path

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[{request_id}] Upload save error: {e}")
        raise HTTPException(status_code=500, detail="Failed to save upload")

@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get a conversation's messages"""
    messages = conversation_manager.get_conversation(conversation_id)
    if not messages:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"conversation_id": conversation_id, "messages": messages}
