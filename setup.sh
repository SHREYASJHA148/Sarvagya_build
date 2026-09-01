#!/bin/bash
# Sarvagya Full-Stack Setup Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Sarvagya - AI Trading Chart Analysis${NC}"
echo -e "${GREEN}Full-Stack Setup${NC}"
echo -e "${GREEN}========================================${NC}\n"

# Check if API key is set
if [ -z "$GOOGLE_API_KEY" ]; then
    echo -e "${YELLOW}⚠️  GOOGLE_API_KEY not set in environment${NC}"
    echo "Set it with: export GOOGLE_API_KEY='YOUR_GEMINI_API_KEY'"
    echo ""
fi

# Backend setup
echo -e "${GREEN}1. Setting up backend...${NC}"
cd backend

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate venv
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo "Installing backend dependencies..."
pip install -q -r requirements.txt

echo -e "${GREEN}✓ Backend ready${NC}\n"

# Frontend setup
echo -e "${GREEN}2. Setting up frontend...${NC}"
cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install -q
fi

echo -e "${GREEN}✓ Frontend ready${NC}\n"

# Instructions
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo -e "${GREEN}========================================\n${NC}"

echo -e "To run Sarvagya:\n"
echo -e "${YELLOW}Terminal 1 (Backend):${NC}"
echo "cd backend"
echo "export GOOGLE_API_KEY='your-api-key'"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    echo "source venv/Scripts/activate"
else
    echo "source venv/bin/activate"
fi
echo "python main.py"
echo ""

echo -e "${YELLOW}Terminal 2 (Frontend):${NC}"
echo "cd frontend"
echo "npm run dev"
echo ""

echo -e "Then open ${YELLOW}http://localhost:3000${NC} in your browser"
