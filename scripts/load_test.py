"""
IKS 2026 설문조사 300명 동시 제출 부하 테스트 스크립트
FastAPI 비동기 I/O 및 SQLite WAL 모드 고동시성 처리 성능 검증
"""

import time
import random
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "http://127.0.0.1:8000"
SUBMIT_URL = f"{BASE_URL}/api/survey/submit"

SAMPLE_COMPANIES = [
    ("Samsung Electronics", "South Korea", "ko"),
    ("Google LLC", "USA", "en"),
    ("Siemens Energy", "Germany", "en"),
    ("Sony Group", "Japan", "en"),
    ("Hyundai Motor", "South Korea", "ko"),
    ("ASML Korea", "Netherlands", "en"),
    ("TotalEnergies", "France", "en"),
    ("SK hynix", "South Korea", "ko"),
    ("Temasek Holdings", "Singapore", "en"),
    ("LG Energy Solution", "South Korea", "ko")
]


def make_random_payload(user_id: int):
    comp, country, lang = random.choice(SAMPLE_COMPANIES)
    return {
        "lang": lang,
        "company_name": f"{comp} #{user_id}",
        "country": country,
        "q1_overall": random.randint(3, 5),

        "conf_q1": random.randint(3, 5),
        "conf_q2": random.sample(["1", "2", "3", "4"], k=random.randint(1, 3)),
        "conf_q3_rank1": 1,
        "conf_q3_rank2": 2,
        "conf_q3_rank3": 3,
        "conf_q3_other": None,
        "conf_q4": f"Simulated user #{user_id} feedback: Great summit organisation.",

        "reg_q1": random.randint(3, 5),
        "reg_q2": random.randint(3, 5),
        "reg_q3_rank1": 1,
        "reg_q3_rank2": 2,
        "reg_q3_other": None,

        "semi_q1": random.randint(3, 5),
        "semi_q2": ["1", "4"],
        "semi_q3": "Useful tax incentive updates.",

        "max_q1": random.randint(3, 5),
        "max_q2": ["2", "3"],
        "max_q3": "Excellent renewable energy transition discussions.",

        "vc_q1": random.randint(3, 5),
        "vc_q2": ["1", "3"],
        "vc_q3": "Networking sessions were very effective."
    }


def send_submission(user_id: int):
    payload = make_random_payload(user_id)
    t0 = time.time()
    try:
        resp = requests.post(SUBMIT_URL, json=payload, timeout=15)
        duration = time.time() - t0
        return {
            "id": user_id,
            "status": resp.status_code,
            "success": resp.status_code == 201,
            "duration": duration,
            "data": resp.json() if resp.status_code == 201 else resp.text
        }
    except Exception as e:
        return {
            "id": user_id,
            "status": -1,
            "success": False,
            "duration": time.time() - t0,
            "error": str(e)
        }


def run_load_test(total_users: int = 300, max_workers: int = 50):
    print("=" * 60)
    print(f"[START] IKS 2026 Survey Concurrency Load Test")
    print(f"   - Total Submissions : {total_users}")
    print(f"   - Concurrent Workers: {max_workers}")
    print(f"   - Target Endpoint   : {SUBMIT_URL}")
    print("=" * 60)

    start_total = time.time()
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(send_submission, i + 1) for i in range(total_users)]
        for f in as_completed(futures):
            results.append(f.result())

    total_time = time.time() - start_total
    success_count = sum(1 for r in results if r["success"])
    fail_count = total_users - success_count
    durations = [r["duration"] for r in results if r["success"]]

    avg_latency = sum(durations) / len(durations) if durations else 0
    p95_latency = sorted(durations)[int(len(durations) * 0.95)] if durations else 0
    tps = total_users / total_time if total_time > 0 else 0

    print("\n" + "=" * 60)
    print("=== Load Test Results Summary ===")
    print("=" * 60)
    print(f"[OK] Success Count    : {success_count} / {total_users} ({(success_count/total_users)*100:.1f}%)")
    print(f"[ERR] Failed Count    : {fail_count}")
    print(f"[TIME] Total Duration : {total_time:.2f} s")
    print(f"[THROUGHPUT] (TPS)    : {tps:.2f} req/sec")
    print(f"[LATENCY] Avg Response: {avg_latency*1000:.1f} ms")
    print(f"[LATENCY] 95th %tile  : {p95_latency*1000:.1f} ms")
    print("=" * 60)


if __name__ == "__main__":
    import sys
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    run_load_test(total_users=count, max_workers=workers)

