# Vercel 서버리스 함수 진입점: backend/app/main.py의 FastAPI 앱을 그대로 불러온다
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.main import app  # noqa: E402,F401
