"""Same-origin FastAPI backend used by the Vercel frontend deployment."""

import os
import tempfile
import uuid
from typing import Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

app = FastAPI(title="Sarvagya API", version="1.0.0")


class ChatResponse(BaseModel):
    message: str
    conversation_id: str
    request_id: str


conversations: dict[str, list[dict[str, str]]] = {}


@app.get("/api/health")
async def health_check():
    api_key_present = bool(os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"))
    return {
        "status": "healthy",
        "message": "Backend is operational",
        "services": {
            "api": "operational",
            "agent": "configured" if api_key_present else "not_configured",
        },
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(
    message: str = Form(...),
    conversation_id: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
):
    message = message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="AI analysis is not configured. Set GOOGLE_API_KEY in Vercel project settings.",
        )

    if file and file.content_type not in {"image/png", "image/jpeg", "image/webp"}:
        raise HTTPException(status_code=400, detail="Invalid file type. Use PNG, JPG, or WebP.")

    request_id = str(uuid.uuid4())
    conversation_id = conversation_id or str(uuid.uuid4())
    history = conversations.setdefault(conversation_id, [])
    image_bytes = None

    if file:
        image_bytes = await file.read()
        if len(image_bytes) > 4 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="File too large. Maximum upload size is 4MB.")

    history.append({"role": "user", "content": message})
    response = await _analyze(api_key, message, history[:-1], image_bytes, file.content_type if file else None, request_id)
    history.append({"role": "assistant", "content": response})

    return ChatResponse(message=response, conversation_id=conversation_id, request_id=request_id)


@app.get("/api/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    messages = conversations.get(conversation_id)
    if not messages:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"conversation_id": conversation_id, "messages": messages}


async def _analyze(api_key, message, history, image_bytes, mime_type, request_id):
    try:
        from google.adk.agents import LlmAgent
        from google.adk.runners import Runner
        from google.adk.sessions import InMemorySessionService
        from google.genai import types

        agent = LlmAgent(
            name="MasterChartAnalyst",
            model="gemini-2.5-flash",
            instruction="""You are a quantitative technical chart analyst. Analyze the uploaded trading chart or question. Identify patterns, trend, support/resistance and indicators visible. Give one primary action (BUY, SELL, or HOLD), an estimated holding horizon, and concise reasons. State uncertainty when chart evidence is insufficient. This is educational analysis, not financial advice.""",
        )
        session_service = InMemorySessionService()
        session_service.create_session(app_name="sarvagya", user_id="trader", session_id=request_id)
        runner = Runner(agent=agent, app_name="sarvagya", session_service=session_service)

        parts = []
        if image_bytes:
            parts.append(types.Part.from_bytes(data=image_bytes, mime_type=mime_type))
        if history:
            context = "\n".join(f"{turn['role'].title()}: {turn['content']}" for turn in history)
            message = f"Conversation so far:\n{context}\n\nCurrent user request: {message}"
        parts.append(types.Part(text=message))

        events = runner.run(
            user_id="trader",
            session_id=request_id,
            new_message=types.Content(role="user", parts=parts),
        )
        for event in events:
            if event.is_final_response() and event.content and event.content.parts:
                response = event.content.parts[0].text
                if response:
                    return response
        raise RuntimeError("The AI service did not return an analysis.")
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Analysis could not be completed. Please try again.") from exc
