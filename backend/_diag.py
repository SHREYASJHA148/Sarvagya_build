"""Diagnostic script: try to import and start the backend app, print errors."""
import os
import sys
import traceback

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Python:", sys.executable)
print("CWD:", os.getcwd())

# Load env
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("dotenv loaded")
except Exception as e:
    print("dotenv import failed:", e)

print("GOOGLE_API_KEY present:", bool(os.getenv("GOOGLE_API_KEY")))

# Try importing the app
try:
    import main
    print("main imported OK, app:", main.app)
except Exception:
    print("main import FAILED:")
    traceback.print_exc()
    sys.exit(1)

# Try importing deps
for mod in ["fastapi", "uvicorn", "routes.chat", "routes.health", "services.agent_adapter", "schemas.chat"]:
    try:
        __import__(mod)
        print("OK import:", mod)
    except Exception as e:
        print("FAIL import:", mod, "->", e)

print("DIAG DONE")
