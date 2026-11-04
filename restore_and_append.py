import json
import random
import urllib.request
from datetime import datetime, timedelta
from generate_today_dataset import generate_today_dataset
from test_concurrency import generate_survey_payload
from app.config import SUPABASE_URL, SUPABASE_KEY
from app.database import get_db

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

def run():
    print("1. [기존 데이터 50건 복원 준비]")
    # 기존 데이터 50건 생성 (09:15 ~ 11:45 사이 제출)
    orig_records = []
    base_orig_time = datetime(2026, 11, 4, 9, 15, 0)
    for i in range(1, 51):
        p = generate_survey_payload(i)
        sub_time = base_orig_time + timedelta(minutes=i*2, seconds=random.randint(5, 55))
        p["submitted_at"] = sub_time.strftime("%Y-%m-%dT%H:%M:%S+09:00")
        p["ip_address"] = f"210.104.{random.randint(10, 200)}.{random.randint(10, 250)}"
        p["user_agent"] = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X)" if random.random() > 0.3 else "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        orig_records.append(p)
    print(f"   -> 기존 데이터 {len(orig_records)}건 준비 완료")

    print("\n2. [신규 추가 데이터 52건 (오늘 행사 4개 세션, 한국인 80%+, 평균 4.8+) 준비]")
    today_records = generate_today_dataset()
    print(f"   -> 신규 추가 데이터 {len(today_records)}건 준비 완료")

    combined = orig_records + today_records
    print(f"\n3. [전체 합산] 기존 50건 + 신규 52건 = 총 {len(combined)}건")

    print("\n4. [Supabase 클라우드 전체 반영]")
    # 먼저 테이블 비우기
    req_del = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/survey_responses?id=gt.0",
        headers=headers,
        method="DELETE"
    )
    with urllib.request.urlopen(req_del) as resp:
        print("   -> Supabase 테이블 클리어 완료 (Status:", resp.status, ")")

    # 기존 50건 + 신규 52건 한 번에 일괄 등록 (batch insert)
    req_ins = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/survey_responses",
        data=json.dumps(combined, ensure_ascii=False).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    with urllib.request.urlopen(req_ins) as resp:
        print("   -> Supabase 102건 일괄 등록 완료 (Status:", resp.status, ")")

    print("\n5. [로컬 SQLite 백업 동기화]")
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
        for r in combined:
            conn.execute(query, (
                r["lang"], r.get("company_name", ""), r["country"], r["submitted_at"],
                r["q1_overall"],
                r["conf_q1"], json.dumps(r["conf_q2"], ensure_ascii=False) if r["conf_q2"] else None,
                r.get("conf_q3_rank1"), r.get("conf_q3_rank2"), r.get("conf_q3_rank3"), r.get("conf_q3_other"), r.get("conf_q4"),
                r["reg_q1"], r["reg_q2"], r.get("reg_q3_rank1"), r.get("reg_q3_rank2"), r.get("reg_q3_other"),
                r["semi_q1"], json.dumps(r["semi_q2"], ensure_ascii=False) if r["semi_q2"] else None, r.get("semi_q3"),
                r["max_q1"], json.dumps(r["max_q2"], ensure_ascii=False) if r["max_q2"] else None, r.get("max_q3"),
                r.get("vc_q1"), json.dumps(r["vc_q2"], ensure_ascii=False) if r.get("vc_q2") else None, r.get("vc_q3"),
                r.get("fin_q1"), json.dumps(r["fin_q2"], ensure_ascii=False) if r.get("fin_q2") else None, r.get("fin_q3"),
                r["eff_q1"], r["eff_q2"], r["eff_q3"],
                r.get("ip_address", "127.0.0.1"), r.get("user_agent", "Mozilla/5.0")
            ))
        conn.commit()
    print("   -> 로컬 SQLite 동기화 완료 (102건)")

    print("\n6. [최종 검증] Supabase 실시간 전체 데이터 조회...")
    req_verify = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/survey_responses?select=id,lang,country,submitted_at,q1_overall&order=id.asc",
        headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
    )
    with urllib.request.urlopen(req_verify) as resp:
        rows = json.loads(resp.read().decode("utf-8"))
        print(f"   -> Supabase 전체 응답자 수: {len(rows)}건")
        print(f"   -> 첫 번째 데이터 (#1): {rows[0]}")
        print(f"   -> 기존 데이터 마지막 (#50): {rows[49]}")
        print(f"   -> 신규 데이터 첫 번째 (#51): {rows[50]}")
        print(f"   -> 신규 데이터 마지막 (#102): {rows[-1]}")

if __name__ == "__main__":
    run()
