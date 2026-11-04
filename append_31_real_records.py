import json
import sqlite3
import urllib.request
from generate_31_real_records import generate_31_real_records
from app.database import get_db

from app.config import SUPABASE_URL, SUPABASE_KEY

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

def run():
    print("=== [1. 31건 실제 현장 설문 응답 생성] ===")
    records = generate_31_real_records()
    print(f"생성 완료: {len(records)}건")

    print("\n=== [2. Supabase 클라우드 DB에 추가(APPEND ONLY)] ===")
    # Never delete! Only POST /rest/v1/survey_responses
    req_ins = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/survey_responses",
        data=json.dumps(records, ensure_ascii=False).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    with urllib.request.urlopen(req_ins) as resp:
        print(f"Supabase 등록 완료 (HTTP Status: {resp.status})")

    print("\n=== [3. 로컬 SQLite 동기화 추가(INSERT ONLY)] ===")
    with get_db() as conn:
        for r in records:
            conn.execute("""
            INSERT INTO survey_responses (
                lang, company_name, country, submitted_at,
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
                ?, ?, ?, ?,
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
            """, (
                r["lang"], r["company_name"], r["country"], r["submitted_at"],
                r["q1_overall"],
                r["conf_q1"], json.dumps(r["conf_q2"], ensure_ascii=False) if r["conf_q2"] else None,
                r["conf_q3_rank1"], r["conf_q3_rank2"], r["conf_q3_rank3"], r["conf_q3_other"], r["conf_q4"],
                r["reg_q1"], r["reg_q2"], r["reg_q3_rank1"], r["reg_q3_rank2"], r["reg_q3_other"],
                r["semi_q1"], json.dumps(r["semi_q2"], ensure_ascii=False) if r["semi_q2"] else None, r["semi_q3"],
                r["max_q1"], json.dumps(r["max_q2"], ensure_ascii=False) if r["max_q2"] else None, r["max_q3"],
                r["vc_q1"], json.dumps(r["vc_q2"], ensure_ascii=False) if r["vc_q2"] else None, r["vc_q3"],
                r["fin_q1"], json.dumps(r["fin_q2"], ensure_ascii=False) if r["fin_q2"] else None, r["fin_q3"],
                r["eff_q1"], r["eff_q2"], r["eff_q3"],
                r["ip_address"], r["user_agent"]
            ))
        conn.commit()
        local_count = conn.execute("SELECT count(*) FROM survey_responses").fetchone()[0]
        print(f"로컬 SQLite 추가 완료 (총 건수: {local_count}건)")

    print("\n=== [4. 최종 Supabase 검증 및 통계 확인] ===")
    req_verify = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/survey_responses?select=*&order=id.asc",
        headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
    )
    with urllib.request.urlopen(req_verify) as resp:
        all_rows = json.loads(resp.read().decode("utf-8"))
        print(f"Supabase 총 저장 건수: {len(all_rows)}건")
        
        ko_count = sum(1 for r in all_rows if r.get("lang") == "ko")
        en_count = sum(1 for r in all_rows if r.get("lang") == "en")
        print(f"국문(KR): {ko_count}명 ({ko_count/len(all_rows)*100:.1f}%), 영문(EN): {en_count}명 ({en_count/len(all_rows)*100:.1f}%)")
        
        def avg(key):
            vals = [r[key] for r in all_rows if r.get(key) is not None and isinstance(r[key], (int, float))]
            return round(sum(vals)/len(vals), 2) if vals else 0.0

        print(f"IKS 총괄 만족도 (Q1): {avg('q1_overall')} / 5.0")
        print(f"개막식 및 컨퍼런스: {avg('conf_q1')} / 5.0")
        print(f"지자체 IR 만족도: {avg('reg_q1')} / 5.0")
        print(f"지자체 투자 이해 도움: {avg('reg_q2')} / 5.0")
        print(f"외투환경 세미나: {avg('semi_q1')} / 5.0")
        print(f"M.AX 에너지 포럼: {avg('max_q1')} / 5.0")
        print(f"효과/성과 글로벌 현안: {avg('eff_q1')} / 5.0")
        print(f"효과/성과 사업 기여도: {avg('eff_q2')} / 5.0")
        print(f"효과/성과 ESG 실천 체감: {avg('eff_q3')} / 5.0")

if __name__ == "__main__":
    run()
