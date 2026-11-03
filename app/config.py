import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Vercel Serverless 환경 감지 (Vercel에서는 /tmp 만 쓰기 가능)
IS_VERCEL = bool(os.getenv("VERCEL") or os.getenv("NOW_REGION"))

if IS_VERCEL:
    DATA_DIR = Path("/tmp")
else:
    DATA_DIR = BASE_DIR / "data"

try:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
except Exception:
    pass

DB_PATH = os.getenv("DB_PATH", str(DATA_DIR / "survey.db"))
ADMIN_SECRET = os.getenv("ADMIN_SECRET", "iks2026admin")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
