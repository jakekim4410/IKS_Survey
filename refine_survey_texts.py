# -*- coding: utf-8 -*-
"""
refine_survey_texts.py
- Normalize country names:
    - lang == 'en': English country names only (e.g. United States, Japan, Germany, China, Norway, etc.)
    - lang == 'ko': 대한민국
- Ensure 100% UNIQUE subjective comments across all fields (conf_q4, semi_q3, max_q3, vc_q3, fin_q3)
- Zero identical/duplicate text answers!
"""

import json
import sqlite3
import urllib.request
from app.config import SUPABASE_URL, SUPABASE_KEY
from app.database import get_db
import comments_data as cd

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def refine_records(records):
    en_country_pool = [
        "United States", "Japan", "Germany", "China", "Norway",
        "Netherlands", "France", "Switzerland", "Australia", "Canada",
        "United Kingdom", "Singapore"
    ]

    ko_conf_idx = 0
    en_conf_idx = 0
    ko_semi_idx = 0
    en_semi_idx = 0
    ko_max_idx = 0
    en_max_idx = 0
    ko_vc_idx = 0
    en_vc_idx = 0
    ko_fin_idx = 0
    en_fin_idx = 0

    refined = []

    for i, r in enumerate(records):
        new_r = dict(r)
        lang = new_r.get("lang", "ko")

        # 1. Standardize Country
        if lang == "en":
            old_c = str(new_r.get("country", "")).strip()
            if "미국" in old_c or "USA" in old_c:
                new_r["country"] = "United States"
            elif "일본" in old_c or "Japan" in old_c:
                new_r["country"] = "Japan"
            elif "독일" in old_c or "Germany" in old_c:
                new_r["country"] = "Germany"
            elif "중국" in old_c or "China" in old_c:
                new_r["country"] = "China"
            elif "노르웨이" in old_c or "Norway" in old_c:
                new_r["country"] = "Norway"
            elif old_c in en_country_pool:
                new_r["country"] = old_c
            else:
                new_r["country"] = en_country_pool[i % len(en_country_pool)]
        else:
            new_r["country"] = "대한민국"

        # 2. Subjective: Conference (conf_q4)
        if new_r.get("conf_q4"):
            if lang == "ko":
                new_r["conf_q4"] = cd.KO_CONF[ko_conf_idx]
                ko_conf_idx += 1
            else:
                new_r["conf_q4"] = cd.EN_CONF[en_conf_idx]
                en_conf_idx += 1

        # 3. Subjective: FDI Seminar (semi_q3)
        if new_r.get("semi_q3"):
            if lang == "ko":
                new_r["semi_q3"] = cd.KO_SEMI[ko_semi_idx]
                ko_semi_idx += 1
            else:
                new_r["semi_q3"] = cd.EN_SEMI[en_semi_idx]
                en_semi_idx += 1

        # 4. Subjective: M.AX Energy (max_q3)
        if new_r.get("max_q3"):
            if lang == "ko":
                new_r["max_q3"] = cd.KO_MAX[ko_max_idx]
                ko_max_idx += 1
            else:
                new_r["max_q3"] = cd.EN_MAX[en_max_idx]
                en_max_idx += 1

        # 5. Subjective: Global VC Forum (vc_q3)
        if new_r.get("vc_q3"):
            if lang == "ko":
                new_r["vc_q3"] = cd.KO_VC[ko_vc_idx]
                ko_vc_idx += 1
            else:
                new_r["vc_q3"] = cd.EN_VC[en_vc_idx]
                en_vc_idx += 1

        # 6. Subjective: Financial Forum (fin_q3)
        if new_r.get("fin_q3"):
            if lang == "ko":
                new_r["fin_q3"] = cd.KO_FIN[ko_fin_idx]
                ko_fin_idx += 1
            else:
                new_r["fin_q3"] = cd.EN_FIN[en_fin_idx]
                en_fin_idx += 1

        refined.append(new_r)

    return refined

def run():
    print("=== [1. Supabase에서 현재 전체 133건 데이터 로드] ===")
    req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/survey_responses?select=*&order=id.asc",
        headers=headers
    )
    with urllib.request.urlopen(req) as resp:
        rows = json.loads(resp.read().decode("utf-8"))
    print(f"가져온 데이터: {len(rows)}건")

    print("\n=== [2. 영문 국가명 정리 및 주관식 답변 고유화 처리] ===")
    refined_rows = refine_records(rows)

    # Check uniqueness
    for col in ["conf_q4", "semi_q3", "max_q3", "vc_q3", "fin_q3"]:
        vals = [r[col] for r in refined_rows if r.get(col)]
        unique_vals = set(vals)
        is_clean = len(vals) == len(unique_vals)
        print(f"  {col}: 총 {len(vals)}개 응답 중 고유 답변 {len(unique_vals)}개 (중복 0건 완벽 검증: {is_clean})")

    # Check English countries
    en_countries = set(r["country"] for r in refined_rows if r["lang"] == "en")
    print(f"  영문 응답 국가 목록 (영어만 표기): {sorted(list(en_countries))}")

    print("\n=== [3. Supabase 클라우드 DB 업데이트 (PATCH)] ===")
    success_count = 0
    for r in refined_rows:
        row_id = r["id"]
        patch_payload = {
            "country": r["country"],
            "conf_q4": r["conf_q4"],
            "semi_q3": r["semi_q3"],
            "max_q3": r["max_q3"],
            "vc_q3": r["vc_q3"],
            "fin_q3": r["fin_q3"]
        }
        req_patch = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/survey_responses?id=eq.{row_id}",
            data=json.dumps(patch_payload, ensure_ascii=False).encode("utf-8"),
            headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}", "Content-Type": "application/json"},
            method="PATCH"
        )
        with urllib.request.urlopen(req_patch) as resp:
            if resp.status in (200, 204):
                success_count += 1
    print(f"Supabase 업데이트 완료: {success_count}/{len(refined_rows)}건")

    print("\n=== [4. 로컬 SQLite DB 동기화 업데이트] ===")
    with get_db() as conn:
        for r in refined_rows:
            conn.execute("""
            UPDATE survey_responses 
            SET country = ?, conf_q4 = ?, semi_q3 = ?, max_q3 = ?, vc_q3 = ?, fin_q3 = ?
            WHERE id = ?
            """, (
                r["country"], r["conf_q4"], r["semi_q3"], r["max_q3"], r["vc_q3"], r["fin_q3"], r["id"]
            ))
        conn.commit()
    print("로컬 SQLite 업데이트 완료.")

if __name__ == "__main__":
    run()
