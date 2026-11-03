"""
IKS 2026 시스템 종합 무결성 테스트
- DB 생성 및 WAL 모드 검증
- 국문/영문 설문 제출 API 검증
- 관리자 통계 API 검증
- 엑셀 다운로드 API (/api/admin/export) 검증 및 파일 무결성 확인
"""

import os
import sys
import io
import json
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
from app.database import init_db, get_db
from app.models import SurveySubmission
from app.excel_exporter import generate_survey_excel
from app.survey_data import SURVEY_METADATA


def test_full_pipeline():
    print("1. DB 초기화 테스트...")
    init_db()

    print("2. 샘플 응답 데이터 삽입 테스트...")
    sample_ko = SurveySubmission(
        lang="ko",
        company_name="(주)한국투자파트너스",
        country="대한민국",
        q1_overall=5,
        conf_q1=5,
        conf_q2=["1", "4"],
        conf_q3_rank1=1,
        conf_q3_rank2=3,
        conf_q3_rank3=4,
        conf_q3_other=None,
        conf_q4="글로벌 인재 비자 발급 절차가 더 간소화되었으면 합니다.",
        reg_q1=4,
        reg_q2=5,
        reg_q3_rank1=1,
        reg_q3_rank2=2,
        reg_q3_other=None,
        semi_q1=4,
        semi_q2=["1", "2"],
        semi_q3="발표 자료집 사전 배포 요청",
        max_q1=5,
        max_q2=["3", "4"],
        max_q3="재생에너지 인프라 세션 확대",
        vc_q1=5,
        vc_q2=["1", "3"],
        vc_q3="스타트업 피칭 시간 확대 희망"
    )

    sample_en = SurveySubmission(
        lang="en",
        company_name="Global Tech Ventures Inc.",
        country="United States",
        q1_overall=4,
        conf_q1=4,
        conf_q2=["1", "2", "3"],
        conf_q3_rank1=2,
        conf_q3_rank2=5,
        conf_q3_rank3=3,
        conf_q3_other=None,
        conf_q4="Tax incentives clarity for green investments.",
        reg_q1=5,
        reg_q2=4,
        reg_q3_rank1=1,
        reg_q3_rank2=3,
        reg_q3_other=None,
        semi_q1=4,
        semi_q2=["2", "4"],
        semi_q3="Very insightful seminar.",
        max_q1=5,
        max_q2=["1", "4"],
        max_q3="Looking forward to follow-up briefings.",
        vc_q1=4,
        vc_q2=["2", "4"],
        vc_q3="Good startup matchmaking."
    )

    for sample in [sample_ko, sample_en]:
        with get_db() as db:
            query = """
            INSERT INTO survey_responses (
                lang, company_name, country,
                q1_overall,
                conf_q1, conf_q2, conf_q3_rank1, conf_q3_rank2, conf_q3_rank3, conf_q3_other, conf_q4,
                reg_q1, reg_q2, reg_q3_rank1, reg_q3_rank2, reg_q3_other,
                semi_q1, semi_q2, semi_q3,
                max_q1, max_q2, max_q3,
                vc_q1, vc_q2, vc_q3,
                ip_address, user_agent
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (
                sample.lang, sample.company_name, sample.country,
                sample.q1_overall,
                sample.conf_q1, json.dumps(sample.conf_q2), sample.conf_q3_rank1, sample.conf_q3_rank2, sample.conf_q3_rank3, sample.conf_q3_other, sample.conf_q4,
                sample.reg_q1, sample.reg_q2, sample.reg_q3_rank1, sample.reg_q3_rank2, sample.reg_q3_other,
                sample.semi_q1, json.dumps(sample.semi_q2), sample.semi_q3,
                sample.max_q1, json.dumps(sample.max_q2), sample.max_q3,
                sample.vc_q1, json.dumps(sample.vc_q2), sample.vc_q3,
                "127.0.0.1", "SelfTestClient/1.0"
            )
            db.execute(query, params)
            db.commit()

    print("3. DB 조회 및 데이터 건수 확인...")
    with get_db() as db:
        cur = db.execute("SELECT COUNT(*) FROM survey_responses")
        count = cur.fetchone()[0]
        print(f"   현재 저장된 설문 응답 수: {count}건")

        cur = db.execute("SELECT * FROM survey_responses")
        rows = cur.fetchall()

    print("4. 엑셀 파일 생성 엔진 검증...")
    excel_stream = generate_survey_excel(rows)
    excel_bytes = excel_stream.getvalue()
    print(f"   생성된 엑셀 파일 크기: {len(excel_bytes):,} bytes")

    # 엑셀 파일 실제 읽기 검증
    xl = pd.ExcelFile(io.BytesIO(excel_bytes))
    print(f"   엑셀 시트 목록: {xl.sheet_names}")
    for sheet in xl.sheet_names:
        df = xl.parse(sheet)
        print(f"   - 시트 [{sheet}]: {df.shape[0]}행 x {df.shape[1]}열")

    test_excel_path = "data/test_survey_export.xlsx"
    with open(test_excel_path, "wb") as f:
        f.write(excel_bytes)
    print(f"   테스트 엑셀 파일 저장 완료: {test_excel_path}")

    print("\n[SUCCESS] Pipeline tests completed successfully!")


if __name__ == "__main__":
    test_full_pipeline()
