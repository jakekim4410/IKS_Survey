import sys
from pathlib import Path

# Vercel 서버리스 런타임 환경에서 프로젝트 루트 경로를 sys.path에 등록
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from main import app

# Vercel Python WSGI/ASGI 핸들러로 app 노출

