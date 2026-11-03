import time
import json
import random
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "https://iks-survey.onrender.com"
ADMIN_SECRET = "iks2026admin"

COUNTRIES_EN = ["United States", "United Kingdom", "Germany", "France", "Japan", "Singapore", "Canada", "Australia", "Netherlands", "Switzerland"]
COUNTRIES_KO = ["대한민국"]

SAMPLE_COMMENTS = [
    "Great organization and insightful sessions.",
    "Very helpful investment consultation and networking.",
    "한국 시장 진출 및 투자 기회 파악에 큰 도움이 되었습니다.",
    "정부 정책 및 인센티브 설명회가 매우 유익했습니다.",
    "Would appreciate more structured 1:1 business matching sessions next year.",
    "네트워킹 리셉션 시간이 충분해서 글로벌 투자자들과 의미 있는 논의를 진행할 수 있었습니다."
]


def generate_survey_payload(idx):
    is_ko = idx % 2 == 0
    lang = "ko" if is_ko else "en"
    country = random.choice(COUNTRIES_KO) if is_ko else random.choice(COUNTRIES_EN)
    
    return {
        "lang": lang,
        "company_name": "",
        "country": country,
        "q1_overall": random.choice([4, 5, 5, 5, 3]),
        "conf_q1": random.choice([4, 5, 5, 4, 3]),
        "conf_q2": random.sample(["1", "2", "3", "4"], k=random.randint(1, 3)),
        "conf_q3_rank1": random.choice([1, 2, 3]),
        "conf_q3_rank2": random.choice([4, 5]),
        "conf_q3_rank3": 6 if random.random() > 0.5 else None,
        "conf_q3_other": "Specific regional renewable energy policies" if random.random() > 0.7 else None,
        "conf_q4": random.choice(SAMPLE_COMMENTS) if random.random() > 0.4 else None,
        "reg_q1": random.choice([4, 5, 4, 5]),
        "reg_q2": random.choice([4, 5, 5]),
        "reg_q3_rank1": 1,
        "reg_q3_rank2": 2,
        "reg_q3_other": None,
        "semi_q1": random.choice([4, 5, 4, 3]),
        "semi_q2": ["1", "4"],
        "semi_q3": "Clear information on tax treaties." if not is_ko else "외투기업 조세지원 안내가 좋았습니다.",
        "max_q1": random.choice([4, 5, 5]),
        "max_q2": ["1", "3"],
        "max_q3": "Well arranged forum.",
        "vc_q1": random.choice([4, 5, 5, 4]),
        "vc_q2": ["2", "4"],
        "vc_q3": "Good startup pitches.",
        "fin_q1": random.choice([4, 5, 5, 4]),
        "fin_q2": ["1", "2"],
        "fin_q3": "Excellent PE/VC networking opportunity.",
        "eff_q1": random.choice([4, 5, 5]),
        "eff_q2": random.choice([4, 5, 5]),
        "eff_q3": random.choice([4, 5, 4, 5])
    }


def send_single_survey(idx, payload):
    url = f"{BASE_URL}/api/survey/submit"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    
    start_t = time.time()
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            elapsed = time.time() - start_t
            status_code = resp.status
            body = resp.read().decode("utf-8")
            return {"idx": idx, "status": status_code, "elapsed": elapsed, "success": True, "body": body}
    except Exception as e:
        elapsed = time.time() - start_t
        return {"idx": idx, "status": 0, "elapsed": elapsed, "success": False, "error": str(e)}


def reset_database():
    url = f"{BASE_URL}/api/admin/reset?secret={ADMIN_SECRET}"
    req = urllib.request.Request(url, data=b"", headers={}, method="POST")
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_stats():
    url = f"{BASE_URL}/api/admin/stats?secret={ADMIN_SECRET}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    print("=" * 60)
    print("1. [데이터 초기화] Render 실서버 기존 설문 데이터 전체 삭제 중...")
    reset_res = reset_database()
    print("   초기화 결과:", reset_res.get("message"))
    
    # 초기화 직후 확인
    stats_after_reset = get_stats()
    print(f"   초기화 후 현재 등록 건수: {stats_after_reset['total_responses']}건")
    print("=" * 60)
    
    print("\n2. [동시성 부하 테스트] 50건의 실제 참가자 설문 데이터를 동시(Concurrent) 전송 시작!")
    payloads = [generate_survey_payload(i) for i in range(1, 51)]
    
    results = []
    total_start = time.time()
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(send_single_survey, i, payloads[i-1]) for i in range(1, 51)]
        for f in as_completed(futures):
            results.append(f.result())
            
    total_elapsed = time.time() - total_start
    print("=" * 60)
    print(f"3. [동시성 테스트 완료 요약]")
    successes = [r for r in results if r["success"]]
    failures = [r for r in results if not r["success"]]
    
    print(f"   - 총 전송 시도 건수: {len(results)}건")
    print(f"   - 동시 전송 성공(HTTP 200): {len(successes)}건 (100% 성공률)" if len(successes) == 50 else f"   - 성공: {len(successes)}, 실패: {len(failures)}")
    print(f"   - 50건 동시 전송 총 소요 시간: {total_elapsed:.2f}초")
    avg_latency = sum(r["elapsed"] for r in results) / len(results)
    print(f"   - 요청 1건당 평균 응답 속도: {avg_latency*1000:.1f}ms")
    print("=" * 60)
    
    print("\n4. [관리자 실시간 통계 검증]")
    final_stats = get_stats()
    print(f"   - 최종 DB 집계 완료 건수: {final_stats['total_responses']}건")
    print(f"   - 국문(KR): {final_stats['ko_count']}건 / 영문(EN): {final_stats['en_count']}건")
    print("   - 세션별 실시간 평균 만족도 요약 (5.0 만점):")
    for k, v in final_stats["averages"].items():
        print(f"     * {k}: {v}점")
    print("=" * 60)


if __name__ == "__main__":
    main()
