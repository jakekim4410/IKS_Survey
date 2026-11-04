import json
import urllib.request
from generate_today_dataset import generate_today_dataset
from app.database import get_db
from app.config import SUPABASE_URL, SUPABASE_KEY

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

def run():
    print("1. [데이터 초기화] Supabase의 기존 테스트 데이터 삭제...")
    req_del = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/survey_responses?id=gt.0",
        headers=headers,
        method="DELETE"
    )
    with urllib.request.urlopen(req_del) as resp:
        print("   Supabase 초기화 완료 (Status:", resp.status, ")")

    print("\n2. [데이터 생성] 오늘 행사 4개 세션 기준 맞춤형 데이터 생성...")
    records = generate_today_dataset()
    print(f"   총 {len(records)}건 생성 완료")

    print("\n3. [데이터 입력] Supabase 클라우드에 52건 등록...")
    req_ins = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/survey_responses",
        data=json.dumps(records, ensure_ascii=False).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    with urllib.request.urlopen(req_ins) as resp:
        print("   Supabase 등록 완료 (Status:", resp.status, ")")

    print("\n4. [로컬 SQLite 동기화] 로컬 백업 DB 동기화...")
    with get_db() as conn:
        conn.execute("DELETE FROM survey_responses;")
        try:
            conn.execute("DELETE FROM sqlite_sequence WHERE name='survey_responses';")
        except Exception:
            pass

        query = """
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
        """
        for r in records:
            conn.execute(query, (
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
    print("   로컬 SQLite 동기화 완료")

    print("\n5. [최종 검증] Supabase 실시간 통계 조회...")
    req_stats = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/survey_responses?select=*&order=id.asc",
        headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
    )
    with urllib.request.urlopen(req_stats) as resp:
        saved = json.loads(resp.read().decode("utf-8"))
        print(f"   -> Supabase 총 등록 건수: {len(saved)}건")
        ko = sum(1 for x in saved if x["lang"] == "ko")
        en = sum(1 for x in saved if x["lang"] == "en")
        print(f"   -> 국문(KR): {ko}건 ({ko/len(saved)*100:.1f}%), 영문(EN): {en}건 ({en/len(saved)*100:.1f}%)")
        
        def calc_avg(col):
            vals = [x[col] for x in saved if x.get(col) is not None]
            return round(sum(vals)/len(vals), 2), len(vals)
            
        print("   -> 총괄 만족도:", calc_avg("q1_overall"))
        print("   -> 컨퍼런스:", calc_avg("conf_q1"))
        print("   -> 지자체IR 만족도:", calc_avg("reg_q1"))
        print("   -> 지자체IR 투자이해:", calc_avg("reg_q2"))
        print("   -> 외투세미나:", calc_avg("semi_q1"))
        print("   -> M.AX에너지 포럼:", calc_avg("max_q1"))
        print("   -> 글로벌 현안 (6-1):", calc_avg("eff_q1"))
        print("   -> 향후 사업 (6-2):", calc_avg("eff_q2"))
        print("   -> ESG 실천 (6-3):", calc_avg("eff_q3"))

if __name__ == "__main__":
    run()
