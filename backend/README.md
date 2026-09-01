# Sarvagya Backend

Backend for the Sarvagya AI trading chart analysis application.

## Setup

```bash
cd backend
pip install -r requirements.txt
export GOOGLE_API_KEY="your-key-here"
python main.py
```

## API Endpoints

- `GET /api/health` - Health check
- `POST /api/chat` - Send message + optional chart image
- `GET /api/conversations/{id}` - Get conversation history

## Architecture

- `main.py` - FastAPI app entry point
- `routes/` - API endpoints
- `services/agent_adapter.py` - Adapter for agent.py
- `schemas/` - Pydantic models
