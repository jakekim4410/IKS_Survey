"""
신규 6-1, 6-2 문항이 포함된 샘플 응답 2건 DB 삽입 스크립트
"""

import sys
import json
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import init_db, get_db

SAMPLE_1_KO = {
    "lang": "ko",
    "company_name": "(주)솔루션테크 코리아",
    "country": "대한민국",
    "q1_overall": 5,
    "conf_q1": 5,
    "conf_q2": ["1", "4"],
    "conf_q3_rank1": 1,
    "conf_q3_rank2": 2,
    "conf_q3_rank3": 4,
    "conf_q3_other": None,
    "conf_q4": "외국인 핵심 엔지니어 비자 심사 기간이 조금 더 단축되면 좋겠습니다.",
    "reg_q1": 4,
    "reg_q2": 5,
    "reg_q3_rank1": 1,
    "reg_q3_rank2": 3,
    "reg_q3_other": None,
    "semi_q1": 4,
    "semi_q2": ["1", "2"],
    "semi_q3": "외투기업 인센티브 관련 일대일 법률/세무 상담 부스 신설 제안",
    "max_q1": 5,
    "max_q2": ["3", "4"],
    "max_q3": "재생에너지 그리드망 연계 관련 정책 논의가 매우 유익했습니다.",
    "vc_q1": 5,
    "vc_q2": ["1", "4"],
    "vc_q3": "유망 스타트업과 글로벌 CVC 간의 후속 매칭 프로그램 지속 희망",
    "eff_q1": 5,  # 6-1 매우 만족(추천)
    "eff_q2": 5   # 6-2 매우 만족(추천)
}

SAMPLE_2_EN = {
    "lang": "en",
    "company_name": "Vanguard CleanTech Investments Ltd.",
    "country": "United Kingdom",
    "q1_overall": 4,
    "conf_q1": 4,
    "conf_q2": ["2", "3"],
    "conf_q3_rank1": 2,
    "conf_q3_rank2": 5,
    "conf_q3_rank3": 1,
    "conf_q3_other": None,
    "conf_q4": "More transparency in regional regulatory compliance processes.",
    "reg_q1": 5,
    "reg_q2": 4,
    "reg_q3_rank1": 2,
    "reg_q3_rank2": 4,
    "reg_q3_other": None,
    "semi_q1": 4,
    "semi_q2": ["3", "4"],
    "semi_q3": "Digital handouts and simultaneous translation headset quality was commendable.",
    "max_q1": 5,
    "max_q2": ["1", "4"],
    "max_q3": "Excellent insights into Korean offshore wind and battery ecosystem.",
    "vc_q1": 4,
    "vc_q2": ["2", "4"],
    "vc_q3": "Startup pitching sessions were well managed and highly informative.",
    "eff_q1": 4,  # 6-1 Agree
    "eff_q2": 5   # 6-2 Strongly agree
}


def insert_samples():
    init_db()

    query = """
    INSERT INTO survey_responses (
        lang, company_name, country,
        q1_overall,
        conf_q1, conf_q2, conf_q3_rank1, conf_q3_rank2, conf_q3_rank3, conf_q3_other, conf_q4,
        reg_q1, reg_q2, reg_q3_rank1, reg_q3_rank2, reg_q3_other,
        semi_q1, semi_q2, semi_q3,
        max_q1, max_q2, max_q3,
        vc_q1, vc_q2, vc_q3,
        eff_q1, eff_q2,
        ip_address, user_agent
    ) VALUES (
        ?, ?, ?,
        ?,
        ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?,
        ?, ?, ?,
        ?, ?, ?,
        ?, ?, ?,
        ?, ?,
        ?, ?
    )
    """

    with get_db() as conn:
        for s in [SAMPLE_1_KO, SAMPLE_2_EN]:
            params = (
                s["lang"], s["company_name"], s["country"],
                s["q1_overall"],
                s["conf_q1"], json.dumps(s["conf_q2"], ensure_ascii=False), s["conf_q3_rank1"], s["conf_q3_rank2"], s["conf_q3_rank3"], s["conf_q3_other"], s["conf_q4"],
                s["reg_q1"], s["reg_q2"], s["reg_q3_rank1"], s["reg_q3_rank2"], s["reg_q3_other"],
                s["semi_q1"], json.dumps(s["semi_q2"], ensure_ascii=False), s["semi_q3"],
                s["max_q1"], json.dumps(s["max_q2"], ensure_ascii=False), s["max_q3"],
                s["vc_q1"], json.dumps(s["vc_q2"], ensure_ascii=False), s["vc_q3"],
                s["eff_q1"], s["eff_q2"],
                "127.0.0.1", "SampleDataLoader/1.0"
            )
            cur = conn.execute(query, params)
            print(f"[OK] Inserted sample #{cur.lastrowid}: {s['company_name']} ({s['lang']})")
        conn.commit()

        # 전체 건수 확인
        cur = conn.execute("SELECT COUNT(*) FROM survey_responses")
        total = cur.fetchone()[0]
        print(f"[TOTAL] Total responses in DB: {total}")


if __name__ == "__main__":
    insert_samples()
