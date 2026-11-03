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

# .env 파일이 존재할 경우 자동 로드
env_file = BASE_DIR / ".env"
if env_file.exists():
    try:
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k, v = k.strip(), v.strip().strip("'\"")
                    if k and k not in os.environ:
                        os.environ[k] = v
    except Exception:
        pass

DB_PATH = os.getenv("DB_PATH", str(DATA_DIR / "survey.db"))
ADMIN_SECRET = os.getenv("ADMIN_SECRET", "iks2026admin")
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://htmhksedluvdrjipffpl.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
