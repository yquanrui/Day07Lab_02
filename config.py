import os, sys
from pathlib import Path
from dotenv import load_dotenv
 
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")
 
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")
DB_NAME = os.getenv("DB_NAME", "review_history.db")
 
if not GEMINI_API_KEY:
    print("Configuration Error: GEMINI_API_KEY environment variable is missing!")
    sys.exit(1)