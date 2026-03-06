# config/settings.py
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()  # optional .env file support

ROOT = Path(__file__).resolve().parents[1]  # project root
DATA_DIR = ROOT / "data"
ASSETS_DIR = ROOT / "assets"
USER_CHATS_DIR = DATA_DIR / "user_chats"

# External API keys (set as environment variables or create .env)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")  # optional
JUDGE0_API_URL = os.getenv("JUDGE0_API_URL", "")  # optional
JUDGE0_API_KEY = os.getenv("JUDGE0_API_KEY", "")  # optional (RapidAPI etc)

# default language
DEFAULT_LANGUAGE = "en"

# Ensure data folders exist
for d in (DATA_DIR, USER_CHATS_DIR, ASSETS_DIR):
    d.mkdir(parents=True, exist_ok=True)