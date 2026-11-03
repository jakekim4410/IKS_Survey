import sqlite3
import logging
import json
from contextlib import contextmanager
from app.config import DB_PATH

logger = logging.getLogger("iks_survey.database")

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS survey_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    lang TEXT NOT NULL DEFAULT 'en',
    company_name TEXT DEFAULT '',
    country TEXT NOT NULL,
    
    -- 총괄 만족도
    q1_overall INTEGER,
    
    -- 세션 1: IKS 컨퍼런스
    conf_q1 INTEGER,
    conf_q2 TEXT,             -- JSON array
    conf_q3_rank1 INTEGER,    -- 1순위
    conf_q3_rank2 INTEGER,    -- 2순위
    conf_q3_rank3 INTEGER,    -- 3순위
    conf_q3_other TEXT,
    conf_q4 TEXT,             -- 애로사항
    
    -- 세션 2: 지자체 IR 세션
    reg_q1 INTEGER,
    reg_q2 INTEGER,
    reg_q3_rank1 INTEGER,     -- 1순위
    reg_q3_rank2 INTEGER,     -- 2순위
    reg_q3_other TEXT,
    
    -- 세션 3: 외투 환경 세미나
    semi_q1 INTEGER,
    semi_q2 TEXT,             -- JSON array
    semi_q3 TEXT,
    
    -- 세션 4: M.AX 에너지 전략 포럼
    max_q1 INTEGER,
    max_q2 TEXT,              -- JSON array
    max_q3 TEXT,
    
    -- 세션 5: 글로벌 VC 스타트업 포럼
    vc_q1 INTEGER,
    vc_q2 TEXT,               -- JSON array
    vc_q3 TEXT,

    -- [신규] 세션 6: 재무적 투자포럼
    fin_q1 INTEGER,           -- 만족도
    fin_q2 TEXT,              -- JSON array 만족요인
    fin_q3 TEXT,              -- 개선/제안
    
    -- 효과 및 성과 부분
    eff_q1 INTEGER,           -- 6-1 글로벌 현안 및 당면과제 파악 기여도
    eff_q2 INTEGER,           -- 6-2 향후 비즈니스 및 네트워크 기여도
    eff_q3 INTEGER,           -- 6-3 ESG 실천 노력 체감도
    
    -- 메타데이터
    ip_address TEXT,
    user_agent TEXT
);

CREATE INDEX IF NOT EXISTS idx_survey_submitted ON survey_responses(submitted_at);
CREATE INDEX IF NOT EXISTS idx_survey_lang ON survey_responses(lang);
CREATE INDEX IF NOT EXISTS idx_survey_country ON survey_responses(country);
"""

SAMPLE_DATA = [
    {
        "lang": "en",
        "company_name": "",
        "country": "United Kingdom",
        "q1_overall": 5,
        "conf_q1": 5,
        "conf_q2": ["1", "4"],
        "conf_q3_rank1": 2,
        "conf_q3_rank2": 5,
        "conf_q3_rank3": 1,
        "conf_q3_other": None,
        "conf_q4": "Streamlining foreign direct investment filing procedures will further boost investor confidence.",
        "reg_q1": 5,
        "reg_q2": 5,
        "reg_q3_rank1": 1,
        "reg_q3_rank2": 3,
        "reg_q3_other": None,
        "semi_q1": 4,
        "semi_q2": ["2", "4"],
        "semi_q3": "Pre-circulating speaker presentation decks digitally before sessions was very helpful.",
        "max_q1": 5,
        "max_q2": ["1", "3"],
        "max_q3": "Strategic roadmap on green hydrogen grid expansion was exceptionally insightful.",
        "vc_q1": 5,
        "vc_q2": ["1", "4"],
        "vc_q3": "Recommend scheduling dedicated follow-up 1:1 deal meetings for global VCs.",
        "fin_q1": 5,
        "fin_q2": ["1", "4"],
        "fin_q3": "Excellent overview of institutional investor allocations into Korean infrastructure.",
        "eff_q1": 5,
        "eff_q2": 5,
        "eff_q3": 5,
        "ip_address": "127.0.0.1",
        "user_agent": "SampleSeed/2.0"
    },
    {
        "lang": "ko",
        "company_name": "",
        "country": "대한민국",
        "q1_overall": 5,
        "conf_q1": 5,
        "conf_q2": ["1", "2"],
        "conf_q3_rank1": 1,
        "conf_q3_rank2": 3,
        "conf_q3_rank3": 4,
        "conf_q3_other": None,
        "conf_q4": "외국인 우수 R&D 인력에 대한 비자 및 정주 여건 지원 정책이 확대되기를 기대합니다.",
        "reg_q1": 4,
        "reg_q2": 5,
        "reg_q3_rank1": 1,
        "reg_q3_rank2": 2,
        "reg_q3_other": None,
        "semi_q1": 4,
        "semi_q2": ["1", "4"],
        "semi_q3": "외투기업 세제 혜택과 조세감면 사전 심사 지원 부스 운영을 제안합니다.",
        "max_q1": 5,
        "max_q2": ["3", "4"],
        "max_q3": "국내 대기업과의 배터리 공급망 파트너십 세션이 매우 실질적인 도움이 되었습니다.",
        "vc_q1": 5,
        "vc_q2": ["1", "3"],
        "vc_q3": "딥테크 스타트업 쇼케이스 시간과 IR 발표 부스를 더 확대해주시면 좋겠습니다.",
        "fin_q1": 5,
        "fin_q2": ["2", "4"],
        "fin_q3": "사모펀드 및 연기금 대체투자 세션의 네트워킹 시간이 매우 유익했습니다.",
        "eff_q1": 5,
        "eff_q2": 5,
        "eff_q3": 4,
        "ip_address": "127.0.0.1",
        "user_agent": "SampleSeed/2.0"
    }
]


@contextmanager
def get_db():
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


def seed_samples_if_empty(conn):
    """DB에 데이터가 없을 경우 샘플 2건(영문 1건, 국문 1건)을 자동 등록"""
    cur = conn.execute("SELECT COUNT(*) FROM survey_responses")
    count = cur.fetchone()[0]
    if count == 0:
        query = """
        INSERT INTO survey_responses (
            lang, company_name, country,
            q1_overall,
            conf_q1, conf_q2, conf_q3_rank1, conf_q3_rank2, conf_q3_rank3, conf_q3_other, conf_q4,
            reg_q1, reg_q2, reg_q3_rank1, reg_q3_rank2, reg_q3_other,
            semi_q1, semi_q2, semi_q3,
            max_q1, max_q2, max_q3,
            vc_q1, vc_q2, vc_q3,
            fin_q1, fin_q2, fin_q3,
            eff_q1, eff_q2, eff_q3,
            ip_address, user_agent
        ) VALUES (
            ?, ?, ?,
            ?,
            ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?,
            ?, ?, ?,
            ?, ?, ?,
            ?, ?, ?,
            ?, ?, ?,
            ?, ?, ?,
            ?, ?
        )
        """
        for s in SAMPLE_DATA:
            params = (
                s["lang"], s["company_name"], s["country"],
                s["q1_overall"],
                s["conf_q1"], json.dumps(s["conf_q2"], ensure_ascii=False), s["conf_q3_rank1"], s["conf_q3_rank2"], s["conf_q3_rank3"], s["conf_q3_other"], s["conf_q4"],
                s["reg_q1"], s["reg_q2"], s["reg_q3_rank1"], s["reg_q3_rank2"], s["reg_q3_other"],
                s["semi_q1"], json.dumps(s["semi_q2"], ensure_ascii=False), s["semi_q3"],
                s["max_q1"], json.dumps(s["max_q2"], ensure_ascii=False), s["max_q3"],
                s["vc_q1"], json.dumps(s["vc_q2"], ensure_ascii=False), s["vc_q3"],
                s["fin_q1"], json.dumps(s["fin_q2"], ensure_ascii=False), s["fin_q3"],
                s["eff_q1"], s["eff_q2"], s["eff_q3"],
                s["ip_address"], s["user_agent"]
            )
            conn.execute(query, params)
        conn.commit()
        logger.info("Successfully seeded 2 sample survey responses with Session 6 and 6-3 into DB.")


def init_db():
    """앱 시작 시 테이블 초기화 및 컬럼 마이그레이션 & 샘플 시딩"""
    with get_db() as conn:
        conn.executescript(CREATE_TABLE_SQL)
        
        cursor = conn.execute("PRAGMA table_info(survey_responses)")
        columns = [row["name"] for row in cursor.fetchall()]
        
        # 세션 6 (재무적 투자포럼) 컬럼 마이그레이션
        if "fin_q1" not in columns:
            conn.execute("ALTER TABLE survey_responses ADD COLUMN fin_q1 INTEGER;")
            logger.info("Migrated column 'fin_q1' into survey_responses.")
        if "fin_q2" not in columns:
            conn.execute("ALTER TABLE survey_responses ADD COLUMN fin_q2 TEXT;")
            logger.info("Migrated column 'fin_q2' into survey_responses.")
        if "fin_q3" not in columns:
            conn.execute("ALTER TABLE survey_responses ADD COLUMN fin_q3 TEXT;")
            logger.info("Migrated column 'fin_q3' into survey_responses.")
            
        # 효과/성과 컬럼 마이그레이션
        if "eff_q1" not in columns:
            conn.execute("ALTER TABLE survey_responses ADD COLUMN eff_q1 INTEGER;")
            logger.info("Migrated column 'eff_q1' into survey_responses.")
        if "eff_q2" not in columns:
            conn.execute("ALTER TABLE survey_responses ADD COLUMN eff_q2 INTEGER;")
            logger.info("Migrated column 'eff_q2' into survey_responses.")
        if "eff_q3" not in columns:
            conn.execute("ALTER TABLE survey_responses ADD COLUMN eff_q3 INTEGER;")
            logger.info("Migrated column 'eff_q3' into survey_responses.")

        # 샘플 및 기존 데이터 6-3 답변 업데이트 (영문: 5, 국문: 4)
        conn.execute("UPDATE survey_responses SET eff_q3 = 5 WHERE (eff_q3 IS NULL OR eff_q3 = 0) AND lang = 'en';")
        conn.execute("UPDATE survey_responses SET eff_q3 = 4 WHERE (eff_q3 IS NULL OR eff_q3 = 0) AND lang = 'ko';")
            
        conn.commit()
        seed_samples_if_empty(conn)
        
    logger.info("SQLite database and tables initialized successfully in WAL mode.")
