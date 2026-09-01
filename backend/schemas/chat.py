"""
Pydantic schemas for chat API
"""
from pydantic import BaseModel, Field
from typing import Optional

class ChatRequest(BaseModel):
    """Request schema for chat endpoint"""
    message: str = Field(..., min_length=1, description="User message")
    conversation_id: Optional[str] = Field(None, description="Optional conversation ID")

class ChatResponse(BaseModel):
    """Response schema for chat endpoint"""
    message: str = Field(..., description="Assistant response")
    conversation_id: str = Field(..., description="Conversation ID")
    request_id: str = Field(..., description="Request tracking ID")
    analysis: Optional[dict] = Field(None, description="Structured analysis if available")

class ErrorResponse(BaseModel):
    """Error response schema"""
    error: str = Field(..., description="Error message")
    request_id: Optional[str] = Field(None, description="Request ID for debugging")
