import urllib.request
import json
import sqlite3
from app.config import SUPABASE_URL, SUPABASE_KEY
from app.database import get_db

headers = {'apikey': SUPABASE_KEY, 'Authorization': f'Bearer {SUPABASE_KEY}'}
req = urllib.request.Request(f'{SUPABASE_URL}/rest/v1/survey_responses?select=*&order=id.asc', headers=headers)
with urllib.request.urlopen(req) as resp:
    rows = json.loads(resp.read().decode('utf-8'))

print(f"Fetched {len(rows)} rows from Supabase.")

with get_db() as conn:
    conn.execute("DELETE FROM survey_responses;")
    try:
        conn.execute("DELETE FROM sqlite_sequence WHERE name='survey_responses';")
    except Exception:
        pass

    for r in rows:
        conn.execute("""
        INSERT INTO survey_responses (
            id, lang, company_name, country, submitted_at,
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
            ?, ?, ?, ?, ?,
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
            r["id"], r["lang"], r["company_name"], r["country"], r["submitted_at"],
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
    print("Local SQLite synchronized with Supabase: 133 rows.")
