# Sarvagya - AI Trading Chart Analysis

Professional ChatGPT-style interface for AI-powered trading chart analysis using the Google ADK and Gemini.

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Google API Key for Gemini access

### Setup

**Unix/Linux/Mac:**
```bash
bash setup.sh
```

**Windows:**
```bash
setup.bat
```

### Run

**Backend (Terminal 1):**
```bash
cd backend
export GOOGLE_API_KEY="your-api-key-here"  # or set GOOGLE_API_KEY=...
source venv/bin/activate  # Windows: venv\Scripts\activate
python main.py
```

**Frontend (Terminal 2):**
```bash
cd frontend
npm run dev
```

Then open [http://localhost:3000](http://localhost:3000) in your browser.

## Product Overview

Sarvagya provides a clean, professional interface for analyzing trading charts with AI intelligence.

**Features:**
- Upload trading charts (PNG, JPG, WebP)
- Ask natural language questions about patterns and trends
- Get AI-powered analysis with candlestick patterns, support/resistance levels, and recommendations
- Conversational follow-ups within the same session
- Real-time loading states and error handling
- Responsive design for desktop and mobile

**Golden User Flow:**
1. Open Sarvagya
2. Upload a trading chart
3. Ask a question like "Analyze this chart and explain the market structure"
4. See real AI analysis
5. Ask follow-up questions
6. Start a new chat when ready

## Architecture

### Backend
- **Framework:** FastAPI
- **Agent:** Google ADK with Gemini 2.5 Flash
- **Storage:** In-memory conversations (session-based)
- **API:** RESTful with multipart file upload

**Key Files:**
- `main.py` - FastAPI application
- `routes/chat.py` - Chat and analysis endpoints
- `services/agent_adapter.py` - Integration with agent.py
- `schemas/chat.py` - Request/response models

### Frontend
- **Framework:** React 18 + Vite
- **Styling:** CSS with design tokens
- **API Client:** Axios with proxy to backend

**Key Files:**
- `src/App.jsx` - Main application
- `src/components/ChatContainer.jsx` - Chat UI component
- `src/api.js` - API client

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | Health check |
| `/api/chat` | POST | Send message + optional chart |
| `/api/conversations/{id}` | GET | Get conversation history |

## Environment Variables

- `GOOGLE_API_KEY` - Google API key for Gemini access (required)

## Technical Details

### Chart Analysis Flow
1. User uploads chart (PNG/JPG/WebP)
2. Frontend validates: type, size < 10MB
3. Request sent to `/api/chat` with multipart data
4. Backend validates upload again
5. Chart passed to Google ADK agent
6. Agent analyzes with Gemini 2.5 Flash
7. Analysis returned to frontend as real response
8. No fake or hardcoded data

### Response Format
The agent returns natural language analysis covering:
- Candlestick patterns identified
- Trend direction and timeframe
- Support and resistance levels
- Trade recommendation (BUY/SELL/HOLD)
- Confidence level and rationale

### Error Handling
- Invalid file types → User-friendly message
- File too large → Suggest smaller file
- Backend unavailable → Retry option
- Agent timeout → Preserve message and allow retry
- Malformed response → Graceful fallback

### Safety & Compliance
- Disclaimer: "AI-generated analysis is for informational and educational purposes and is not guaranteed financial advice"
- No fake analysis results
- No misleading guarantee claims
- Server-side validation of all uploads
- Secrets never exposed to frontend

## Performance

- UI responds immediately on send
- Loading indicator shows while agent processes
- Typical analysis latency: 5-15 seconds
- No blocking operations in browser
- Responsive at desktop and mobile sizes

## Testing

### Manual Test Checklist
- [ ] Text-only message
- [ ] Chart + question
- [ ] Follow-up question in same conversation
- [ ] New Chat clears state
- [ ] Retry on error
- [ ] Invalid file rejected
- [ ] Oversized file rejected
- [ ] Backend down handled gracefully
- [ ] Mobile responsive
- [ ] Desktop layout looks professional

### Demo Script
1. Open clean Sarvagya
2. Show empty state with example prompts
3. Upload a trading chart
4. Ask: "Analyze this chart and explain the market structure"
5. Show processing state
6. Show real agent response
7. Ask follow-up: "What pattern do you see?"
8. Demonstrate conversation context
9. New Chat → resets cleanly

## Known Limitations

- Conversation history is session-only (not persisted between restarts)
- No user authentication
- No trading execution capabilities
- Analysis depends on Google API availability and key validity

## File Structure

```
sarvagya_build/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment variables (add GOOGLE_API_KEY here)
│   ├── routes/
│   │   ├── chat.py            # Chat endpoints
│   │   └── health.py          # Health check
│   ├── services/
│   │   └── agent_adapter.py   # Agent integration
│   └── schemas/
│       └── chat.py            # Pydantic models
├── frontend/
│   ├── package.json           # Node dependencies
│   ├── index.html             # HTML entry
│   ├── vite.config.js         # Build config
│   └── src/
│       ├── App.jsx            # Main component
│       ├── api.js             # API client
│       ├── index.css          # Global styles
│       └── components/
│           └── ChatContainer.jsx  # Chat UI
├── setup.sh                    # Setup script (Unix)
├── setup.bat                   # Setup script (Windows)
└── README.md                   # This file
```

## Troubleshooting

**Frontend can't connect to backend:**
- Ensure backend is running on `localhost:8000`
- Check CORS is enabled (should be by default)
- Check browser console for errors

**Agent analysis fails:**
- Verify `GOOGLE_API_KEY` environment variable is set correctly
- Check backend logs for detailed error
- Try with a different chart image

**File upload fails:**
- Verify file is PNG, JPG, or WebP
- Ensure file size < 10MB
- Check server filesystem has write permissions

## Demo Positioning

Sarvagya is a professional AI research tool for traders and students, not a trading bot or automation platform. It helps understand chart patterns and technical structure through conversational AI, similar to ChatGPT but specialized for trading analysis.

**One-liner:** "AI-powered conversational analysis of trading charts"

**Elevator pitch:** "Upload a chart, ask questions, and get real-time technical analysis from an AI expert. Understand patterns, levels, and scenarios with a natural conversation instead of complex indicators."

---

Built for the Hackathon. Powered by Google ADK and Gemini.
