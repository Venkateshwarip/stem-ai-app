# backend/chat_manager.py
import json
from pathlib import Path
import config.settings as settings
from datetime import datetime
import uuid

USER_CHATS_FILE = settings.USER_CHATS_DIR / "chats.json"

def _ensure():
    settings.USER_CHATS_DIR.mkdir(parents=True, exist_ok=True)
    if not USER_CHATS_FILE.exists():
        with USER_CHATS_FILE.open("w", encoding="utf-8") as f:
            json.dump({}, f)

def save_chat(subject: str, user_id: str, message: str, reply: str):
    _ensure()
    with USER_CHATS_FILE.open("r+", encoding="utf-8") as f:
        data = json.load(f)
        data.setdefault(user_id, [])
        data[user_id].append({
            "id": str(uuid.uuid4()),
            "subject": subject,
            "message": message,
            "reply": reply,
            "ts": datetime.utcnow().isoformat()
        })
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()
    return True

def list_chats(user_id: str):
    _ensure()
    with USER_CHATS_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get(user_id, [])

def delete_chat(user_id: str, chat_id: str):
    _ensure()
    with USER_CHATS_FILE.open("r+", encoding="utf-8") as f:
        data = json.load(f)
        user_chats = data.get(user_id, [])
        user_chats = [c for c in user_chats if c.get("id") != chat_id]
        data[user_id] = user_chats
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()
    return True