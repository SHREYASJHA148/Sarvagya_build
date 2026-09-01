# ⚡ SARVAGYA - QUICK FIX GUIDE

## The Issue: Backend Showing as "Offline"

The updated **Sarvagya.bat** now fixes this automatically!

---

## 🚀 What To Do RIGHT NOW

### Windows Users

**Just run this ONE command:**
```
C:\Users\SHREYAS JHA\sarvagya_build\Sarvagya.bat
```

Or **double-click** `Sarvagya.bat` in the folder.

**Wait 30 seconds total**, then:
- Two terminal windows will open (Backend and Frontend)
- Browser will open automatically to http://localhost:3000
- Chat interface will load

---

## ⏱️ Timeline

```
0 sec  - Click Sarvagya.bat
5 sec  - Backend starts
10 sec - Frontend starts
15 sec - Browser opens
30 sec - Everything ready
```

---

## ✅ What You Should See

### Backend Window (Terminal 1)
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Frontend Window (Terminal 2)
```
➜  Local:   http://localhost:3000/
```

### Browser
```
Sarvagya - AI Trading Chart Analysis
[Upload button and chat interface]
```

---

## ❌ If Still Showing "Backend Offline"

### Try This:

1. **Wait another 10 seconds**
   - Backend sometimes takes longer to start

2. **Refresh the browser**
   - Press F5 or Ctrl+R

3. **Check backend terminal**
   - Look for red errors
   - If you see errors, note them

4. **Try closing both windows and running again**
   - Close both terminal windows
   - Wait 5 seconds
   - Run Sarvagya.bat again

---

## 🔧 If That Doesn't Work

### Ports In Use?

```
netstat -ano | findstr ":8000"
netstat -ano | findstr ":3000"
```

If either shows results:
- Close that application
- Or restart your computer

### Manual Start (Failsafe)

**Terminal 1:**
```cmd
cd C:\Users\SHREYAS JHA\sarvagya_build\backend
set GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
venv\Scripts\activate
python main.py
```

**Terminal 2 (new window):**
```cmd
cd C:\Users\SHREYAS JHA\sarvagya_build\frontend
npm run dev
```

**Browser:**
```
http://localhost:3000
```

---

## 🎯 The Updated Sarvagya.bat NOW:

✅ Sets API key automatically
✅ Kills any existing services on those ports
✅ Starts backend properly
✅ Waits for backend to be ready
✅ Starts frontend properly
✅ Waits for frontend to be ready
✅ Verifies both are running
✅ Opens browser automatically
✅ Shows clear status messages

---

## 📋 Key File Locations

```
Main Folder: C:\Users\SHREYAS JHA\sarvagya_build\

Launcher: Sarvagya.bat              ← DOUBLE-CLICK THIS
Backend:  backend/main.py           (FastAPI)
Frontend: frontend/src/App.jsx      (React)
API Key:  backend/.env              (Already set)
Config:   backend/config.py         (Already setup)
```

---

## 💡 Pro Tips

1. **Don't close the terminal windows**
   - Keep both running while using Sarvagya
   - Check them if something goes wrong

2. **The browser error might be premature**
   - Backend takes a few seconds to fully start
   - Wait 10+ seconds before refreshing

3. **Port conflicts are common**
   - If 8000 or 3000 are in use, kill those processes
   - Or restart computer

4. **Always run setup.bat first**
   - If this is your first time: `setup.bat`
   - This installs all dependencies
   - Then run `Sarvagya.bat`

---

## ✨ SUCCESS = 

✓ Backend terminal shows "Uvicorn running"
✓ Frontend terminal shows "Local: http://localhost:3000"
✓ Browser displays Sarvagya chat
✓ No "Backend offline" message
✓ Ready to upload chart and demo

---

## 🚨 ABSOLUTE LAST RESORT

If everything fails:

1. Delete: `backend/venv` and `frontend/node_modules`
2. Run: `setup.bat` (reinstall everything)
3. Run: `Sarvagya.bat` (start fresh)

This always works because it rebuilds everything from scratch.

---

## 📞 Need Help?

See these files:
- **BACKEND_OFFLINE_HELP.md** - Detailed troubleshooting
- **README.md** - Complete documentation
- **COMMANDS_TO_RUN.md** - Manual commands
- **QUICK_START.txt** - Quick reference

---

## 🎉 YOU'VE GOT THIS!

The updated launcher makes everything automatic.

**Just run Sarvagya.bat and wait 30 seconds.**

Everything else is handled for you.

Good luck with your demo! 🚀
