import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from app.config import ADMIN_SECRET
from app.database import get_db
from app.models import SurveySubmission, SubmissionResponse
from app.excel_exporter import generate_survey_excel
from app.survey_data import SURVEY_METADATA

router = APIRouter(prefix="/api")


def verify_admin_key(request: Request):
    token = request.query_params.get("secret") or request.headers.get("X-Admin-Secret")
    if token != ADMIN_SECRET:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="관리자 인증 키가 유효하지 않습니다. (Invalid Admin Secret)"
        )
    return True


@router.get("/survey/schema")
def get_survey_schema():
    """국문/영문 설문 메타데이터 및 문항 정보 제공"""
    return SURVEY_METADATA


@router.post("/survey/submit", response_model=SubmissionResponse, status_code=status.HTTP_201_CREATED)
def submit_survey(submission: SurveySubmission, request: Request):
    """
    모바일/웹 설문 응답 저장 API (FastAPI Threadpool + SQLite WAL 모드 활용)
    동시 접속 300+명 요청을 락 경합 없이 신속하게 처리
    """
    ip_addr = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")

    conf_q2_json = json.dumps(submission.conf_q2, ensure_ascii=False) if submission.conf_q2 else None
    semi_q2_json = json.dumps(submission.semi_q2, ensure_ascii=False) if submission.semi_q2 else None
    max_q2_json = json.dumps(submission.max_q2, ensure_ascii=False) if submission.max_q2 else None
    vc_q2_json = json.dumps(submission.vc_q2, ensure_ascii=False) if submission.vc_q2 else None

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

    params = (
        submission.lang, submission.company_name, submission.country,
        submission.q1_overall,
        submission.conf_q1, conf_q2_json, submission.conf_q3_rank1, submission.conf_q3_rank2, submission.conf_q3_rank3, submission.conf_q3_other, submission.conf_q4,
        submission.reg_q1, submission.reg_q2, submission.reg_q3_rank1, submission.reg_q3_rank2, submission.reg_q3_other,
        submission.semi_q1, semi_q2_json, submission.semi_q3,
        submission.max_q1, max_q2_json, submission.max_q3,
        submission.vc_q1, vc_q2_json, submission.vc_q3,
        submission.eff_q1, submission.eff_q2,
        ip_addr, user_agent
    )

    try:
        with get_db() as conn:
            cursor = conn.execute(query, params)
            conn.commit()
            inserted_id = cursor.lastrowid
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"설문 저장 중 오류가 발생했습니다: {str(e)}"
        )

    msg = "설문 응답이 성공적으로 제출되었습니다. 감사합니다." if submission.lang == "ko" else "Your survey response has been successfully submitted. Thank you."
    return SubmissionResponse(
        success=True,
        id=inserted_id,
        message=msg
    )


@router.get("/admin/export")
def export_survey_excel(auth: bool = Depends(verify_admin_key)):
    """
    [3단계] 관리자 전용 엑셀 다운로드 API
    DB 전체 응답 기록을 .xlsx 파일로 변환하여 다운로드 제공
    """
    with get_db() as conn:
        cursor = conn.execute("SELECT * FROM survey_responses ORDER BY id ASC")
        rows = cursor.fetchall()

    excel_stream = generate_survey_excel(rows)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"IKS2026_Survey_Responses_{timestamp}.xlsx"

    headers = {
        "Content-Disposition": f'attachment; filename="{filename}"',
        "Access-Control-Expose-Headers": "Content-Disposition"
    }

    return Response(
        content=excel_stream.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers
    )


@router.get("/admin/stats")
def get_admin_stats(auth: bool = Depends(verify_admin_key)):
    """관리자 대시보드 실시간 통계 KPI API"""
    with get_db() as conn:
        cur = conn.execute("SELECT COUNT(*) FROM survey_responses")
        total_count = cur.fetchone()[0]

        cur = conn.execute("SELECT COUNT(*) FROM survey_responses WHERE lang = 'ko'")
        ko_count = cur.fetchone()[0]

        cur = conn.execute("SELECT COUNT(*) FROM survey_responses WHERE lang = 'en'")
        en_count = cur.fetchone()[0]

        cur = conn.execute("""
            SELECT 
                AVG(q1_overall) as avg_overall,
                AVG(conf_q1) as avg_conf,
                AVG(reg_q1) as avg_reg,
                AVG(reg_q2) as avg_reg_help,
                AVG(semi_q1) as avg_semi,
                AVG(max_q1) as avg_max,
                AVG(vc_q1) as avg_vc,
                AVG(eff_q1) as avg_eff_q1,
                AVG(eff_q2) as avg_eff_q2
            FROM survey_responses
        """)
        row = cur.fetchone()
        averages = {
            "overall": round(row["avg_overall"], 2) if row["avg_overall"] else None,
            "conf": round(row["avg_conf"], 2) if row["avg_conf"] else None,
            "reg": round(row["avg_reg"], 2) if row["avg_reg"] else None,
            "reg_help": round(row["avg_reg_help"], 2) if row["avg_reg_help"] else None,
            "semi": round(row["avg_semi"], 2) if row["avg_semi"] else None,
            "max": round(row["avg_max"], 2) if row["avg_max"] else None,
            "vc": round(row["avg_vc"], 2) if row["avg_vc"] else None,
            "eff_q1": round(row["avg_eff_q1"], 2) if row["avg_eff_q1"] else None,
            "eff_q2": round(row["avg_eff_q2"], 2) if row["avg_eff_q2"] else None,
        }

        cur = conn.execute("""
            SELECT id, submitted_at, lang, company_name, country, q1_overall
            FROM survey_responses
            ORDER BY id DESC
            LIMIT 10
        """)
        recent_rows = [dict(r) for r in cur.fetchall()]

    return {
        "total_responses": total_count,
        "ko_count": ko_count,
        "en_count": en_count,
        "averages": averages,
        "recent_responses": recent_rows
    }
