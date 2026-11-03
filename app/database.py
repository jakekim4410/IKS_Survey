import sqlite3
import logging
from contextlib import contextmanager
from app.config import DB_PATH

logger = logging.getLogger("iks_survey.database")

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS survey_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    lang TEXT NOT NULL DEFAULT 'ko',
    company_name TEXT NOT NULL,
    country TEXT NOT NULL,
    
    -- 총괄 만족도
    q1_overall INTEGER,
    
    -- 컨퍼런스 세션
    conf_q1 INTEGER,
    conf_q2 TEXT,             -- JSON array of selected choice numbers e.g. ["1", "3"]
    conf_q3_rank1 INTEGER,    -- 1순위
    conf_q3_rank2 INTEGER,    -- 2순위
    conf_q3_rank3 INTEGER,    -- 3순위
    conf_q3_other TEXT,
    conf_q4 TEXT,             -- 외투기업 애로사항
    
    -- 지자체 IR 세션
    reg_q1 INTEGER,
    reg_q2 INTEGER,
    reg_q3_rank1 INTEGER,     -- 1순위
    reg_q3_rank2 INTEGER,     -- 2순위
    reg_q3_other TEXT,
    
    -- 외투 환경 세미나
    semi_q1 INTEGER,
    semi_q2 TEXT,             -- JSON array
    semi_q3 TEXT,
    
    -- M.AX 에너지 전략 포럼
    max_q1 INTEGER,
    max_q2 TEXT,              -- JSON array
    max_q3 TEXT,
    
    -- 글로벌 VC 스타트업 포럼
    vc_q1 INTEGER,
    vc_q2 TEXT,               -- JSON array
    vc_q3 TEXT,
    
    -- 메타데이터
    ip_address TEXT,
    user_agent TEXT
);

CREATE INDEX IF NOT EXISTS idx_survey_submitted ON survey_responses(submitted_at);
CREATE INDEX IF NOT EXISTS idx_survey_lang ON survey_responses(lang);
CREATE INDEX IF NOT EXISTS idx_survey_company ON survey_responses(company_name);
"""


@contextmanager
def get_db():
    """
    고동시성(300+명 동시 접속) 처리를 위한 SQLite 최적화 컨텍스트 매니저
    - WAL (Write-Ahead Logging) 모드로 읽기/쓰기 락 경합 방지
    - busy_timeout 10,000ms 설정으로 락 대기 시 자동 재시도
    - synchronous=NORMAL로 고성능 비동기 디스크 플러시
    """
    conn = sqlite3.connect(DB_PATH, timeout=20.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA busy_timeout = 10000;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    conn.execute("PRAGMA cache_size = -64000;")
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    """앱 시작 시 테이블 및 인덱스 초기화"""
    with get_db() as conn:
        conn.executescript(CREATE_TABLE_SQL)
        conn.commit()
    logger.info("SQLite database and tables initialized successfully in WAL mode.")
