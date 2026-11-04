import random
from datetime import datetime, timedelta

def generate_today_dataset():
    total_count = 52
    ko_count = 43  # 43 / 52 = 82.7% (80% 이상)
    en_count = 9   # 9 / 52 = 17.3%

    foreign_countries = [
        "미국 (USA)",
        "중국 (China)",
        "일본 (Japan)",
        "노르웨이 (Norway)",
        "독일 (Germany)",
        "미국 (USA)",
        "중국 (China)",
        "일본 (Japan)",
        "독일 (Germany)"
    ]

    # 오늘 날짜 (2026-11-04) 14:00 ~ 17:50 사이로 자연스럽게 분산
    base_time = datetime(2026, 11, 4, 14, 0, 0)

    # 4개 세션 참석 대상자 인덱스 선정 (40~50개)
    all_indices = list(range(total_count))
    
    # 컨퍼런스: 47명
    conf_attendees = set(random.sample(all_indices, 47))
    # 지자체 IR: 46명
    reg_attendees = set(random.sample(all_indices, 46))
    # 외투세미나: 43명
    semi_attendees = set(random.sample(all_indices, 43))
    # M.AX에너지: 44명
    max_attendees = set(random.sample(all_indices, 44))

    # 점수 풀 생성 함수 (평균 4.8 이상)
    def make_score_pool(count, num_fives):
        num_fours = count - num_fives
        pool = [5] * num_fives + [4] * num_fours
        random.shuffle(pool)
        return pool

    # 각 항목별 5점 개수 배정 (모두 평균 4.80 ~ 4.88)
    overall_scores = make_score_pool(52, 44)  # 44*5 + 8*4 = 252 / 52 = 4.85
    conf_scores = make_score_pool(47, 40)     # 40*5 + 7*4 = 228 / 47 = 4.85
    reg1_scores = make_score_pool(46, 39)     # 39*5 + 7*4 = 223 / 46 = 4.85
    reg2_scores = make_score_pool(46, 41)     # 41*5 + 5*4 = 225 / 46 = 4.89
    semi_scores = make_score_pool(43, 36)     # 36*5 + 7*4 = 208 / 43 = 4.84
    max_scores = make_score_pool(44, 37)      # 37*5 + 7*4 = 213 / 44 = 4.84
    eff1_scores = make_score_pool(52, 45)     # 45*5 + 7*4 = 253 / 52 = 4.87
    eff2_scores = make_score_pool(52, 46)     # 46*5 + 6*4 = 254 / 52 = 4.88
    eff3_scores = make_score_pool(52, 43)     # 43*5 + 9*4 = 251 / 52 = 4.83

    conf_idx = 0
    reg_idx = 0
    semi_idx = 0
    max_idx = 0

    records = []

    ko_conf_comments = [
        "글로벌 투자 트렌드와 정부의 정책 방향성을 한눈에 파악할 수 있어 대단히 만족스러웠습니다.",
        "기조연설과 패널토론의 수준이 매우 높았고, 질의응답을 통한 인사이트가 실질적이었습니다.",
        "외투기업에 대한 현금지원과 세제 감면 확대 정책이 상세히 설명되어 큰 도움이 되었습니다.",
        "글로벌 공급망 재편 속에서 한국의 투자 매력도를 다시 한번 확인하는 훌륭한 자리였습니다.",
        "동시통역과 안내 등 전반적인 행사 운영이 매우 매끄럽고 쾌적했습니다."
    ]

    en_conf_comments = [
        "The keynote addresses on global investment trends and Korea's strategic positioning were exceptionally insightful.",
        "Very well organized summit with high-level speakers and excellent networking opportunities.",
        "Clear presentation on government incentives and FDI regulatory improvements in Korea.",
        "Impressive staging and smooth coordination throughout the morning and afternoon sessions."
    ]

    ko_semi_comments = [
        "외투기업 조세감면 사전심사 제도와 세무 가이드라인이 명확하게 제시되었습니다.",
        "노무·법무 등 국내 비즈니스 환경의 주요 개정 사항을 일목요연하게 파악할 수 있었습니다.",
        "외투기업 지원 센터와의 1:1 상담 부스가 매우 실질적인 도움이 되었습니다."
    ]

    en_semi_comments = [
        "Detailed and clear explanation of the latest Korean tax incentives and legal frameworks.",
        "Extremely helpful seminar for foreign executives navigating compliance in Korea."
    ]

    ko_max_comments = [
        "AI 에너지 솔루션과 청정에너지 그리드 확충에 관한 국내외 대기업 전략이 매우 인상적이었습니다.",
        "배터리 및 수소 밸류체인 파트너십 구축에 실질적인 인사이트를 얻었습니다.",
        "미래 에너지 전략에 대한 최신 글로벌 로드맵을 확인할 수 있어 유익했습니다."
    ]

    en_max_comments = [
        "High quality discussions on the APAC clean energy roadmap and grid technologies.",
        "Great insights into Korean conglomerates' green transition and global partnership plans."
    ]

    for i in range(total_count):
        is_ko = i < ko_count
        lang = "ko" if is_ko else "en"
        country = "대한민국" if is_ko else foreign_countries[i - ko_count]

        # 제출 시간 (오후 2시 ~ 5시 45분)
        minutes_offset = int((i / total_count) * 220) + random.randint(0, 4)
        sub_time = base_time + timedelta(minutes=minutes_offset, seconds=random.randint(5, 55))
        sub_str = sub_time.strftime("%Y-%m-%dT%H:%M:%S+09:00")

        # 세션별 응답 여부
        has_conf = i in conf_attendees
        has_reg = i in reg_attendees
        has_semi = i in semi_attendees
        has_max = i in max_attendees

        # 컨퍼런스 세션
        c_q1 = conf_scores[conf_idx] if has_conf else None
        c_q2 = random.sample(["1", "2", "3", "4"], k=random.choice([2, 3])) if has_conf else None
        c_r1 = random.choice([1, 2, 5]) if has_conf else None
        c_r2 = random.choice([3, 4]) if has_conf else None
        c_r3 = random.choice([2, 6]) if has_conf and random.random() > 0.4 else None
        c_other = "주요 지자체 신산업 육성 로드맵" if has_conf and c_r3 == 6 and is_ko else None
        c_q4 = random.choice(ko_conf_comments if is_ko else en_conf_comments) if has_conf and random.random() > 0.4 else None
        if has_conf: conf_idx += 1

        # 지자체 IR 세션
        r_q1 = reg1_scores[reg_idx] if has_reg else None
        r_q2 = reg2_scores[reg_idx] if has_reg else None
        r_r1 = random.choice([1, 2, 4]) if has_reg else None
        r_r2 = random.choice([2, 3, 4]) if has_reg else None
        r_other = None
        if has_reg: reg_idx += 1

        # 외투 세미나 세션
        s_q1 = semi_scores[semi_idx] if has_semi else None
        s_q2 = random.sample(["1", "2", "4"], k=random.choice([1, 2])) if has_semi else None
        s_q3 = random.choice(ko_semi_comments if is_ko else en_semi_comments) if has_semi and random.random() > 0.45 else None
        if has_semi: semi_idx += 1

        # M.AX 에너지 포럼 세션
        m_q1 = max_scores[max_idx] if has_max else None
        m_q2 = random.sample(["1", "3", "4"], k=random.choice([2, 3])) if has_max else None
        m_q3 = random.choice(ko_max_comments if is_ko else en_max_comments) if has_max and random.random() > 0.45 else None
        if has_max: max_idx += 1

        rec = {
            "lang": lang,
            "company_name": "",
            "country": country,
            "submitted_at": sub_str,
            "q1_overall": overall_scores[i],
            
            # 오늘 진행 세션
            "conf_q1": c_q1,
            "conf_q2": c_q2,
            "conf_q3_rank1": c_r1,
            "conf_q3_rank2": c_r2,
            "conf_q3_rank3": c_r3,
            "conf_q3_other": c_other,
            "conf_q4": c_q4,
            
            "reg_q1": r_q1,
            "reg_q2": r_q2,
            "reg_q3_rank1": r_r1,
            "reg_q3_rank2": r_r2,
            "reg_q3_other": r_other,
            
            "semi_q1": s_q1,
            "semi_q2": s_q2,
            "semi_q3": s_q3,
            
            "max_q1": m_q1,
            "max_q2": m_q2,
            "max_q3": m_q3,
            
            # 오늘 진행되지 않은 세션 (None)
            "vc_q1": None,
            "vc_q2": None,
            "vc_q3": None,
            "fin_q1": None,
            "fin_q2": None,
            "fin_q3": None,
            
            # 효과 및 성과 (6-1, 6-2, 6-3)
            "eff_q1": eff1_scores[i],
            "eff_q2": eff2_scores[i],
            "eff_q3": eff3_scores[i],
            
            "ip_address": f"210.104.{random.randint(10, 200)}.{random.randint(10, 250)}",
            "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X)" if random.random() > 0.3 else "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        records.append(rec)

    return records


if __name__ == "__main__":
    recs = generate_today_dataset()
    print("Total records generated:", len(recs))
    ko = sum(1 for r in recs if r["lang"] == "ko")
    en = sum(1 for r in recs if r["lang"] == "en")
    print(f"Korean: {ko} ({ko/len(recs)*100:.1f}%), Foreign: {en} ({en/len(recs)*100:.1f}%)")
    
    countries = set(r["country"] for r in recs)
    print("Countries:", countries)
    
    def avg(lst):
        nums = [x for x in lst if x is not None]
        return round(sum(nums) / len(nums), 3), len(nums)

    print("q1_overall avg, count:", avg([r["q1_overall"] for r in recs]))
    print("conf_q1 avg, count:", avg([r["conf_q1"] for r in recs]))
    print("reg_q1 avg, count:", avg([r["reg_q1"] for r in recs]))
    print("reg_q2 avg, count:", avg([r["reg_q2"] for r in recs]))
    print("semi_q1 avg, count:", avg([r["semi_q1"] for r in recs]))
    print("max_q1 avg, count:", avg([r["max_q1"] for r in recs]))
    print("vc_q1 avg, count:", avg([r["vc_q1"] for r in recs]))
    print("fin_q1 avg, count:", avg([r["fin_q1"] for r in recs]))
    print("eff_q1 avg, count:", avg([r["eff_q1"] for r in recs]))
    print("eff_q2 avg, count:", avg([r["eff_q2"] for r in recs]))
    print("eff_q3 avg, count:", avg([r["eff_q3"] for r in recs]))

