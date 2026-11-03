import os
import json
import logging
import urllib.request
import urllib.error
from typing import List, Dict, Any, Optional
from app.config import SUPABASE_URL, SUPABASE_KEY

logger = logging.getLogger("iks_survey.supabase")

SUPABASE_URL = SUPABASE_URL.rstrip("/")


def is_supabase_enabled() -> bool:
    return bool(SUPABASE_URL and SUPABASE_KEY)


def _supabase_request(endpoint: str, method: str = "GET", payload: Any = None, prefer: Optional[str] = None) -> Any:
    url = f"{SUPABASE_URL}/rest/v1/{endpoint}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    if prefer:
        headers["Prefer"] = prefer

    data = None
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            resp_bytes = resp.read()
            if not resp_bytes:
                return None
            return json.loads(resp_bytes.decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        logger.error(f"Supabase HTTP {e.code} error on {method} {url}: {err_msg}")
        raise RuntimeError(f"Supabase error ({e.code}): {err_msg}")
    except Exception as e:
        logger.error(f"Supabase network error on {method} {url}: {e}")
        raise


def insert_response(record: Dict[str, Any]) -> int:
    """Supabase survey_responses 테이블에 새 응답 저장 후 생성된 id 반환"""
    res = _supabase_request(
        endpoint="survey_responses",
        method="POST",
        payload=record,
        prefer="return=representation"
    )
    if isinstance(res, list) and len(res) > 0:
        return res[0].get("id")
    elif isinstance(res, dict) and "id" in res:
        return res["id"]
    return 1


def fetch_all_responses() -> List[Dict[str, Any]]:
    """Supabase survey_responses 테이블의 전체 데이터 조회 (Excel 내보내기용)"""
    res = _supabase_request("survey_responses?select=*&order=id.asc", method="GET")
    return res if isinstance(res, list) else []


def reset_all_responses() -> None:
    """Supabase survey_responses 테이블의 모든 응답 삭제 (0건 리셋)"""
    _supabase_request("survey_responses?id=gt.0", method="DELETE")


def get_stats() -> Dict[str, Any]:
    """Supabase 데이터 기반 실시간 통계 계산"""
    rows = fetch_all_responses()
    total_count = len(rows)
    ko_count = sum(1 for r in rows if r.get("lang") == "ko")
    en_count = sum(1 for r in rows if r.get("lang") == "en")

    def calc_avg(key: str) -> Optional[float]:
        vals = [r[key] for r in rows if r.get(key) is not None and isinstance(r[key], (int, float))]
        return round(sum(vals) / len(vals), 2) if vals else None

    averages = {
        "overall": calc_avg("q1_overall"),
        "conf": calc_avg("conf_q1"),
        "reg": calc_avg("reg_q1"),
        "reg_help": calc_avg("reg_q2"),
        "semi": calc_avg("semi_q1"),
        "max": calc_avg("max_q1"),
        "vc": calc_avg("vc_q1"),
        "fin": calc_avg("fin_q1"),
        "eff_q1": calc_avg("eff_q1"),
        "eff_q2": calc_avg("eff_q2"),
        "eff_q3": calc_avg("eff_q3"),
    }

    # 최근 10건 (최신순)
    sorted_rows = sorted(rows, key=lambda x: x.get("id") or 0, reverse=True)
    recent_responses = []
    for r in sorted_rows[:10]:
        recent_responses.append({
            "id": r.get("id"),
            "submitted_at": str(r.get("submitted_at") or "")[:19].replace("T", " "),
            "lang": r.get("lang"),
            "country": r.get("country"),
            "q1_overall": r.get("q1_overall")
        })

    return {
        "total_responses": total_count,
        "ko_count": ko_count,
        "en_count": en_count,
        "averages": averages,
        "recent_responses": recent_responses
    }
