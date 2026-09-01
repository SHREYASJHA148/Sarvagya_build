# SARVAGYA - BACKEND NOT STARTING? TROUBLESHOOTING

## Quick Fix

The updated **Sarvagya.bat** now:
- ✅ Starts BOTH backend and frontend
- ✅ Waits for both to initialize
- ✅ Verifies services are running
- ✅ Opens browser automatically

---

## If You Still See "Backend Offline"

### Step 1: Check the Backend Terminal Window

When you run `Sarvagya.bat`, TWO windows should open:

**Backend Window Should Show:**
```
INFO:     Started server process [####]
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Frontend Window Should Show:**
```
➜  Local:   http://localhost:3000/
➜  press h to show help
```

If you see errors in the backend window, note them and continue to Step 2.

---

### Step 2: Verify API Key is Set

The updated script automatically sets:
```
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

If you see "API key not configured" error:
1. Check backend/.env file has GOOGLE_API_KEY
2. It should contain: `GOOGLE_API_KEY=YOUR_GEMINI_API_KEY`

---

### Step 3: Check Ports

If backend still won't start, the ports might be in use.

**Check if port 8000 is free:**
```
netstat -ano | findstr ":8000"
```

**Check if port 3000 is free:**
```
netstat -ano | findstr ":3000"
```

If ports are in use:
1. Close any other applications using those ports
2. Run: `Sarvagya.bat` again

---

### Step 4: Manual Start (If Launcher Fails)

If `Sarvagya.bat` still doesn't work, start manually:

**Terminal 1 - Backend:**
```cmd
cd C:\Users\SHREYAS JHA\sarvagya_build\backend
set GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
venv\Scripts\activate
python main.py
```

**Terminal 2 - Frontend:**
```cmd
cd C:\Users\SHREYAS JHA\sarvagya_build\frontend
npm run dev
```

Wait for both to show "running" messages, then open:
```
http://localhost:3000
```

---

### Step 5: Check Backend Logs

**In backend terminal, you should see no red errors.**

Common issues:

**Error: "module not found"**
- Solution: Run `setup.bat` first to install dependencies

**Error: "Port 8000 already in use"**
- Solution: Change port or kill existing process
- Check: `netstat -ano | findstr ":8000"`

**Error: "API key invalid"**
- Solution: Verify GOOGLE_API_KEY is set correctly
- Check: `echo %GOOGLE_API_KEY%` in terminal

---

### Step 6: Verify Health Check

Once backend is running, test it directly:

**In your browser, go to:**
```
http://localhost:8000/api/health
```

Should show:
```json
{
  "status": "healthy",
  "message": "Backend is operational",
  "services": {
    "api": "operational",
    "agent": "configured"
  }
}
```

If you see this, backend is working!

---

## Fresh Start (Recommended)

If nothing works, try a complete fresh start:

1. **Close everything**
   - Close all terminal windows
   - Close browser

2. **Run setup again**
   ```
   setup.bat
   ```
   Wait for it to complete

3. **Run launcher**
   ```
   Sarvagya.bat
   ```
   Wait 30 seconds total

4. **Open browser**
   ```
   http://localhost:3000
   ```

---

## The Updated Sarvagya.bat Does:

✅ Sets API key automatically
✅ Kills any existing services on ports 8000 and 3000
✅ Starts backend in one window
✅ Waits 10 seconds for backend to initialize
✅ Starts frontend in another window
✅ Waits 15 seconds for frontend to initialize
✅ Verifies both services are running
✅ Opens browser automatically
✅ Shows clear status messages

---

## Still Having Issues?

**Check these files in order:**
1. backend/main.py - FastAPI setup
2. backend/.env - API key configuration
3. backend/requirements.txt - Dependencies
4. backend/routes/chat.py - Chat endpoint

All should be present and correct.

---

## Emergency: Run Without Launcher

If `Sarvagya.bat` fails completely, use manual commands:

**Terminal 1:**
```
cd backend
venv\Scripts\activate
set GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
python main.py
```

**Terminal 2:**
```
cd frontend
npm run dev
```

This always works if dependencies are installed.

---

## Success Indicators

**Backend Running:**
- Terminal shows "Uvicorn running on http://0.0.0.0:8000"
- http://localhost:8000/api/health returns JSON
- No red errors in terminal

**Frontend Running:**
- Terminal shows "Local: http://localhost:3000/"
- Browser displays Sarvagya chat interface
- No errors in browser console

**Ready to Demo:**
- Both terminals show "running" messages
- Browser shows chat with upload button
- Upload a chart and test

---

## Next Steps

1. Run the updated **Sarvagya.bat**
2. Check both terminal windows for "running" messages
3. Browser should open automatically
4. If "backend offline" error appears:
   - Wait 5 more seconds
   - Refresh browser (Ctrl+R or Cmd+R)
5. If still offline, follow troubleshooting above

---

**The updated launcher should solve the issue!**
It now ensures both services start properly before opening the browser.

Good luck! 🚀
