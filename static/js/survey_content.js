const SURVEY_TRANSLATIONS = {
  ko: {
    badge_event: "IKS 2026",
    badge_survey: "참가자 만족도 설문",
    title: "2026 Invest KOREA Summit 참가자 설문 조사",
    intro_desc: "Invest KOREA에서는 IKS 2026 참가자를 대상으로 설문조사를 실시하고 있습니다.\n설문 결과는 사업 성과분석, 향후 개선 및 발전을 위해 활용되며, 응답 내용 및 개인정보는 법에 따라 철저히 보호되고 통계 목적으로만 사용될 예정입니다. 협조해주셔서 대단히 감사드립니다.",
    
    sec_info: "기본 정보",
    label_country: "소재 국가",
    ph_country: "국가명을 입력해주세요 (예: 대한민국, 미국, 일본 등)",
    
    sec_overall: "총괄 만족도",
    // 1. 요청 반영: 문1 문항제목 변경
    q1_overall_title: "문1. Invest KOREA 2026의 전반적인 만족도",
    
    sec_conf: "IKS 컨퍼런스",
    // 2. 요청 반영: 문2-1, 문2-2 문항제목 변경
    conf_q1_title: "문2-1. IKS 컨퍼런스의 전반적인 만족도는 어떻습니까?",
    conf_q2_title: "문2-2. IKS 컨퍼런스에서 가장 만족스러웠던 점은 무엇입니까?",
    sub_multi: "(복수 선택 가능)",
    conf_q3_title: "문2-3. 향후 컨퍼런스에서 반드시 다루어졌으면 하는 내용은 무엇입니까?",
    sub_rank3: "(중요한 순으로 최대 3개까지 터치하여 순위 선택)",
    conf_q3_ph_other: "기타 희망 내용을 입력해주세요",
    conf_q4_title: "문2-4. (외투기업 대상) 국내 사업 경영 중 애로사항이 있으시면 자유롭게 기재하여 주십시오",
    conf_q4_note: "* 단, 기업 간의 사적 분쟁, 개별기업의 영업에 관한 사항, 국제 표준에 반하는 요구는 제외",
    ph_optional: "자유롭게 의견을 남겨주세요 (선택사항)",

    sec_reg: "지자체 투자환경 IR",
    reg_q1_title: "문1. 지자체 투자환경 IR의 전반적인 만족도는 어떻습니까?",
    reg_q2_title: "문2. 지자체 투자환경 IR이 지자체 환경에 대한 이해 또는 투자유치를 확대하는 데 도움이 되었습니까?",
    reg_q3_title: "문3. 지자체 투자환경 IR의 상담 성과를 제고하기 위해 개선되어야 할 사항은 무엇입니까?",
    sub_rank2: "(중요한 순으로 최대 2개까지 터치하여 순위 선택)",
    reg_q3_ph_other: "기타 개선사항을 입력해주세요",

    sec_semi: "외투 환경 세미나",
    semi_q1_title: "문1. 외투 환경 세미나의 전반적인 만족도는 어떻습니까?",
    semi_q2_title: "문2. 외투 환경 세미나에서 가장 만족스러웠던 점은 무엇입니까?",
    semi_q3_title: "문3. 외투 환경 세미나에서 개선 또는 제안하고 싶은 사항은 무엇입니까?",

    sec_max: "M.AX 에너지 전략 포럼",
    max_q1_title: "문1. M.AX 에너지 전략 포럼의 전반적인 만족도는 어떻습니까?",
    max_q2_title: "문2. M.AX 에너지 전략 포럼에서 가장 만족스러웠던 점은 무엇입니까?",
    max_q3_title: "문3. M.AX 에너지 전략 포럼 중 개선 또는 제안하고 싶은 사항은 무엇입니까?",

    sec_vc: "글로벌 VC 스타트업 포럼",
    vc_q1_title: "문1. 글로벌 VC 스타트업 포럼의 전반적인 만족도는 어떻습니까?",
    vc_q2_title: "문2. 글로벌 VC 스타트업 포럼에서 가장 만족스러웠던 점은 무엇입니까?",
    vc_q3_title: "문3. 글로벌 VC 스타트업 포럼 중 개선 또는 제안하고 싶은 사항은 무엇입니까?",

    // 4. 요청 반영: 세션 6 재무적 투자포럼
    sec_fin: "재무적 투자포럼",
    fin_q1_title: "문1. 재무적 투자포럼의 전반적인 만족도는 어떻습니까?",
    fin_q2_title: "문2. 재무적 투자포럼에서 가장 만족스러웠던 점은 무엇입니까?",
    fin_q3_title: "문3. 재무적 투자포럼 중 개선 또는 제안하고 싶은 사항은 무엇입니까?",

    // 효과 및 성과 부분
    sec_eff: "효과 및 성과 부분",
    eff_q1_title: "6-1. Invest KOREA Summit 2026이 글로벌 현안과 당면과제를 시의적절하게 파악하는데 도움이 되었다고 생각하십니까?",
    eff_q2_title: "6-2. Invest KOREA Summit 2026을 통해서 확보한 정보, 네트워크 등이 향후에도 귀 사의 사업에 도움이 될 것이라고 생각하십니까?",

    btn_submit: "설문 응답 제출하기",
    btn_submitting: "응답 저장 중...",
    
    success_title: "설문 제출 완료",
    success_desc: "소중한 응답이 안전하게 저장되었습니다.\nInvest KOREA Summit 2026에 참여해주셔서 진심으로 감사드립니다.",
    btn_done: "홈으로 돌아가기",

    scales_satisfaction: [
      { val: 5, text: "매우 만족" },
      { val: 4, text: "만족" },
      { val: 3, text: "보통" },
      { val: 2, text: "불만족" },
      { val: 1, text: "매우 불만족" }
    ],
    scales_agreement: [
      { val: 5, text: "매우 그렇다" },
      { val: 4, text: "그렇다" },
      { val: 3, text: "보통" },
      { val: 2, text: "그렇지 않다" },
      { val: 1, text: "매우 그렇지 않다" }
    ],
    scales_recommendation: [
      { val: 5, text: "매우 만족(추천)" },
      { val: 4, text: "만족" },
      { val: 3, text: "보통" },
      { val: 2, text: "불만" },
      { val: 1, text: "매우 불만(비추천)" }
    ],

    factors: [
      { id: "1", text: "내용의 적정성 (주제와 정보가 내 관심사에 맞았다)" },
      { id: "2", text: "연출의 효과성 (무대·영상·부스 등 시각적 연출이 인상적이었다)" },
      { id: "3", text: "참신함 (기존 투자유치행사와 다른 새로운 시도가 있었다)" },
      { id: "4", text: "실질적 도움 (투자 검토에 바로 사용 가능한 정보나 연결을 얻었다)" }
    ],

    conf_q3_items: [
      { id: 1, text: "정부 관계자에 의한 정책방침 및 변화 발표" },
      { id: 2, text: "산업 전문가에 의한 국내 산업동향 및 전망" },
      { id: 3, text: "기업의 한국 투자사례 강연" },
      { id: 4, text: "한국 대기업의 투자계획, 사업계획, 조달방침 설명" },
      { id: 5, text: "세계적으로 저명한 석학을 초청, FDI/통상/경제전망 등 관련 발표 및 패널 토론" },
      { id: 6, text: "기타 (직접 입력)", isOther: true }
    ],

    reg_q3_items: [
      { id: 1, text: "국내기업과 외국인투자자 간의 보다 타겟화된 매칭" },
      { id: 2, text: "개별 상담 시간의 확대" },
      { id: 3, text: "상담 주선 시스템의 개선" },
      { id: 4, text: "원활한 소통을 위한 통역 서비스 개선" },
      { id: 5, text: "기타 (직접 입력)", isOther: true }
    ],

    rank_label_1: "1순위",
    rank_label_2: "2순위",
    rank_label_3: "3순위",
    validation_req: "소재 국가는 필수 입력 항목입니다."
  },

  en: {
    badge_event: "IKS 2026",
    badge_survey: "Participant Survey",
    title: "2026 Invest KOREA Summit Participant Survey",
    intro_desc: "Invest KOREA is conducting a survey of participants in IKS 2026.\nThe results will be used for performance analysis and for improving and developing future events. Your responses and personal information will be strictly protected in accordance with applicable laws and used for statistical purposes only. Thank you very much for your cooperation.",
    
    sec_info: "Participant Information",
    label_country: "Country",
    ph_country: "Enter country (e.g., USA, Japan, Germany, etc.)",

    sec_overall: "Overall Satisfaction",
    // 1. Updated: Q1 title
    q1_overall_title: "Q1. Overall satisfaction with Invest KOREA 2026",

    sec_conf: "IKS Conference",
    // 2. Updated: Q2-1, Q2-2 titles
    conf_q1_title: "Q2-1. How satisfied are you with the IKS Conference overall?",
    conf_q2_title: "Q2-2. What did you find most satisfying about the IKS Conference?",
    sub_multi: "(Multiple answers allowed)",
    conf_q3_title: "Q2-3. What topics would you like to see covered at future conferences?",
    sub_rank3: "(Select up to 3 by tapping in order of importance)",
    conf_q3_ph_other: "Please specify other topic",
    conf_q4_title: "Q2-4. (For foreign-invested companies) Please feel free to describe any difficulties you face in doing business in Korea.",
    conf_q4_note: "* Excluding private disputes between companies, matters concerning an individual company's business operations, and requests contrary to international standards.",
    ph_optional: "Please leave your comments (Optional)",

    sec_reg: "Regional Government Investment Briefing",
    reg_q1_title: "Q1. How satisfied are you with the Regional Government Investment Briefing overall?",
    reg_q2_title: "Q2. Did the Regional Government Investment Briefing help you better understand the regional investment environment or expand investment attraction?",
    reg_q3_title: "Q3. What should be improved to enhance the outcomes of consultations at Regional Government Investment Briefing?",
    sub_rank2: "(Select up to 2 by tapping in order of importance)",
    reg_q3_ph_other: "Please specify other improvements",

    sec_semi: "Foreign Investment Environment Seminar",
    semi_q1_title: "Q1. How satisfied are you with the Foreign Investment Environment Seminar overall?",
    semi_q2_title: "Q2. What did you find most satisfying about Foreign Investment Environment Seminar?",
    semi_q3_title: "Q3. What improvements or suggestions do you have for the Foreign Investment Environment Seminar?",

    sec_max: "M.AX Energy Strategy Forum",
    max_q1_title: "Q1. How satisfied are you with the M.AX Energy Strategy Forum overall?",
    max_q2_title: "Q2. What did you find most satisfying about the M.AX Energy Strategy Forum?",
    max_q3_title: "Q3. What improvements or suggestions do you have for the M.AX Energy Strategy Forum?",

    sec_vc: "Global VC Startup Forum",
    vc_q1_title: "Q1. How satisfied are you with the Global VC Startup Forum overall?",
    vc_q2_title: "Q2. What did you find most satisfying about the Global VC Startup Forum?",
    vc_q3_title: "Q3. What improvements or suggestions do you have for the Global VC Startup Forum?",

    // 4. Added: Session 6 Financial Investment Forum
    sec_fin: "Financial Investment Forum",
    fin_q1_title: "Q1. How satisfied are you with the Financial Investment Forum overall?",
    fin_q2_title: "Q2. What did you find most satisfying about the Financial Investment Forum?",
    fin_q3_title: "Q3. What improvements or suggestions do you have for the Financial Investment Forum?",

    // Outcomes & Impact
    sec_eff: "Outcomes & Impact",
    eff_q1_title: "6-1. Did Invest KOREA Summit 2026 enhance your understanding of global investment trends and key issues?",
    eff_q2_title: "6-2. Do you expect the information and business connections gained at Invest KOREA Summit 2026 to benefit your future business activities?",

    btn_submit: "Submit Survey",
    btn_submitting: "Submitting...",

    success_title: "Survey Submitted",
    success_desc: "Your responses have been securely recorded.\nThank you very much for your participation in Invest KOREA Summit 2026.",
    btn_done: "Return to Top",

    scales_satisfaction: [
      { val: 5, text: "Very satisfied" },
      { val: 4, text: "Satisfied" },
      { val: 3, text: "Neutral" },
      { val: 2, text: "Dissatisfied" },
      { val: 1, text: "Very dissatisfied" }
    ],
    scales_agreement: [
      { val: 5, text: "Strongly agree" },
      { val: 4, text: "Agree" },
      { val: 3, text: "Neutral" },
      { val: 2, text: "Disagree" },
      { val: 1, text: "Strongly disagree" }
    ],
    scales_recommendation: [
      { val: 5, text: "Strongly agree" },
      { val: 4, text: "Agree" },
      { val: 3, text: "Neutral" },
      { val: 2, text: "Disagree" },
      { val: 1, text: "Strongly disagree" }
    ],

    factors: [
      { id: "1", text: "Relevance of content (The topics and information matched my interests)" },
      { id: "2", text: "Effectiveness of presentation (The stage, videos, booths and other visual elements were impressive)" },
      { id: "3", text: "Novelty (There were new approaches that set this apart from other investment promotion events)" },
      { id: "4", text: "Practical value (I gained information or connections I can use directly in investment review)" }
    ],

    conf_q3_items: [
      { id: 1, text: "Government officials presenting policy directions and changes" },
      { id: 2, text: "Industry experts presenting Korean industry trends and outlook" },
      { id: 3, text: "Companies sharing their investment cases in Korea" },
      { id: 4, text: "Major Korean corporations explaining their investment plans, business plans and procurement policies" },
      { id: 5, text: "Presentations and panel discussions by world-renowned scholars on FDI, trade, economic outlook, etc." },
      { id: 6, text: "Other (Please specify)", isOther: true }
    ],

    reg_q3_items: [
      { id: 1, text: "More targeted matching between Korean companies and foreign investors" },
      { id: 2, text: "Longer individual consultation sessions" },
      { id: 3, text: "Improvement of the consultation arrangement system" },
      { id: 4, text: "Better interpretation services for smoother communication" },
      { id: 5, text: "Other (Please specify)", isOther: true }
    ],

    rank_label_1: "1st",
    rank_label_2: "2nd",
    rank_label_3: "3rd",
    validation_req: "Country is a required field."
  }
};
