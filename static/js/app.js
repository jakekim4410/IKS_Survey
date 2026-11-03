// Invest KOREA Summit 2026 Survey Frontend Logic
// 외국인 참가자가 다수이므로 영문(en) 기본 설정
let currentLang = 'en';

// 순위 선택 상태 저장 (배열 순서가 곧 1순위, 2순위, 3순위)
let confQ3Ranks = []; // max 3
let regQ3Ranks = [];  // max 2

document.addEventListener('DOMContentLoaded', () => {
  initLanguage();
  initFormInteractions();
});

function initLanguage() {
  // 상단 헤더 토글 버튼
  const btnKo = document.getElementById('btnLangKo');
  const btnEn = document.getElementById('btnLangEn');

  if (btnKo) btnKo.addEventListener('click', () => switchLanguage('ko'));
  if (btnEn) btnEn.addEventListener('click', () => switchLanguage('en'));

  // 세그먼트 컨트롤 버튼 바인딩
  document.querySelectorAll('.segment-btn, .lang-choice-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const selected = btn.getAttribute('data-lang');
      if (selected) switchLanguage(selected);
    });
  });

  // 초기 렌더링 (영어 기본)
  applyLanguage(currentLang);
}

function switchLanguage(lang) {
  if (currentLang === lang) return;
  currentLang = lang;

  // 헤더 버튼 상태 동기화
  const btnKo = document.getElementById('btnLangKo');
  const btnEn = document.getElementById('btnLangEn');
  if (btnKo) btnKo.classList.toggle('active', lang === 'ko');
  if (btnEn) btnEn.classList.toggle('active', lang === 'en');

  // 세그먼트 버튼 상태 동기화
  document.querySelectorAll('.segment-btn, .lang-choice-btn').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-lang') === lang);
  });

  applyLanguage(lang);
}

function applyLanguage(lang) {
  const t = SURVEY_TRANSLATIONS[lang];

  // 1. 단순 텍스트 번역 바인딩
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (t[key] !== undefined) {
      el.textContent = t[key];
    }
  });

  // 2. input placeholder 바인딩
  document.querySelectorAll('[data-i18n-ph]').forEach(el => {
    const key = el.getAttribute('data-i18n-ph');
    if (t[key] !== undefined) {
      el.setAttribute('placeholder', t[key]);
    }
  });

  // 3. 5점 척도 라벨 업데이트
  updateScales(lang);

  // 4. 복수 선택 라벨 업데이트
  updateFactors(lang);

  // 5. 순위 선택 항목 라벨 및 배지 텍스트 업데이트
  updateRankItems(lang);
}

function updateScales(lang) {
  const t = SURVEY_TRANSLATIONS[lang];

  // 만족도 척도 (총괄, 컨퍼런스, 지자체IR 만족도, 세미나, MAX, VC)
  document.querySelectorAll('.scale-satisfaction').forEach(container => {
    container.querySelectorAll('.scale-option').forEach(opt => {
      const val = parseInt(opt.getAttribute('data-value'), 10);
      const item = t.scales_satisfaction.find(s => s.val === val);
      if (item) {
        const textEl = opt.querySelector('.scale-text');
        if (textEl) textEl.textContent = item.text;
      }
    });
  });

  // 동의도 척도 (지자체IR 도움 여부)
  document.querySelectorAll('.scale-agreement').forEach(container => {
    container.querySelectorAll('.scale-option').forEach(opt => {
      const val = parseInt(opt.getAttribute('data-value'), 10);
      const item = t.scales_agreement.find(s => s.val === val);
      if (item) {
        const textEl = opt.querySelector('.scale-text');
        if (textEl) textEl.textContent = item.text;
      }
    });
  });

  // 효과/성과 추천 척도 (6-1, 6-2)
  document.querySelectorAll('.scale-recommendation').forEach(container => {
    container.querySelectorAll('.scale-option').forEach(opt => {
      const val = parseInt(opt.getAttribute('data-value'), 10);
      const item = t.scales_recommendation.find(s => s.val === val);
      if (item) {
        const textEl = opt.querySelector('.scale-text');
        if (textEl) textEl.textContent = item.text;
      }
    });
  });

  // ESG 체감도 척도 (6-3)
  document.querySelectorAll('.scale-esg').forEach(container => {
    container.querySelectorAll('.scale-option').forEach(opt => {
      const val = parseInt(opt.getAttribute('data-value'), 10);
      const item = t.scales_esg.find(s => s.val === val);
      if (item) {
        const textEl = opt.querySelector('.scale-text');
        if (textEl) textEl.textContent = item.text;
      }
    });
  });
}

function updateFactors(lang) {
  const t = SURVEY_TRANSLATIONS[lang];
  // 4가지 공통 만족 요인
  document.querySelectorAll('.factors-choice-group').forEach(group => {
    group.querySelectorAll('.choice-item').forEach(item => {
      const id = item.getAttribute('data-id');
      const factor = t.factors.find(f => f.id === id);
      if (factor) {
        item.querySelector('.choice-label').textContent = factor.text;
      }
    });
  });
}

function updateRankItems(lang) {
  const t = SURVEY_TRANSLATIONS[lang];

  // 컨퍼런스 Q2-3
  document.querySelectorAll('#conf_q3_list .rank-item').forEach(item => {
    const id = parseInt(item.getAttribute('data-id'), 10);
    const meta = t.conf_q3_items.find(i => i.id === id);
    if (meta) {
      item.querySelector('.rank-item-text').textContent = meta.text;
    }
  });

  // 지자체 Q3
  document.querySelectorAll('#reg_q3_list .rank-item').forEach(item => {
    const id = parseInt(item.getAttribute('data-id'), 10);
    const meta = t.reg_q3_items.find(i => i.id === id);
    if (meta) {
      item.querySelector('.rank-item-text').textContent = meta.text;
    }
  });

  // 배지 텍스트 언어 변경
  renderRankBadges('conf_q3_list', confQ3Ranks);
  renderRankBadges('reg_q3_list', regQ3Ranks);
}

function initFormInteractions() {
  // 1. 5점 척도 선택 인터랙션
  document.querySelectorAll('.scale-grid').forEach(grid => {
    grid.addEventListener('click', (e) => {
      const opt = e.target.closest('.scale-option');
      if (!opt) return;
      const group = opt.closest('.scale-grid');
      group.querySelectorAll('.scale-option').forEach(o => o.classList.remove('selected'));
      opt.classList.add('selected');
      const radio = opt.querySelector('input[type="radio"]');
      if (radio) radio.checked = true;
    });
  });

  // 2. 복수 선택 체크박스 인터랙션
  document.querySelectorAll('.choice-item').forEach(item => {
    item.addEventListener('click', () => {
      item.classList.toggle('selected');
      const chk = item.querySelector('input[type="checkbox"]');
      if (chk) chk.checked = item.classList.contains('selected');
    });
  });

  // 3. 컨퍼런스 문2-3 순위 선택 (최대 3개)
  document.querySelectorAll('#conf_q3_list .rank-item').forEach(item => {
    item.addEventListener('click', () => {
      const id = parseInt(item.getAttribute('data-id'), 10);
      handleRankClick(id, confQ3Ranks, 3, 'conf_q3_list');
      // 기타 항목 선택 시 텍스트 인풋 토글
      const otherContainer = document.getElementById('conf_q3_other_wrap');
      if (otherContainer) {
        otherContainer.style.display = confQ3Ranks.includes(6) ? 'block' : 'none';
      }
    });
  });

  // 4. 지자체 IR 문3 순위 선택 (최대 2개)
  document.querySelectorAll('#reg_q3_list .rank-item').forEach(item => {
    item.addEventListener('click', () => {
      const id = parseInt(item.getAttribute('data-id'), 10);
      handleRankClick(id, regQ3Ranks, 2, 'reg_q3_list');
      const otherContainer = document.getElementById('reg_q3_other_wrap');
      if (otherContainer) {
        otherContainer.style.display = regQ3Ranks.includes(5) ? 'block' : 'none';
      }
    });
  });

  // 5. 폼 제출 처리
  const form = document.getElementById('iksSurveyForm');
  form.addEventListener('submit', handleFormSubmit);

  // 6. 완료 후 다시하기 버튼
  const btnRestart = document.getElementById('btnRestart');
  if (btnRestart) {
    btnRestart.addEventListener('click', () => {
      window.location.reload();
    });
  }
}

function handleRankClick(id, rankArray, maxItems, containerId) {
  const index = rankArray.indexOf(id);
  if (index >= 0) {
    // 이미 선택된 항목 터치 시 선택 해제
    rankArray.splice(index, 1);
  } else {
    // 신규 선택
    if (rankArray.length >= maxItems) {
      // 최대 허용 개수 도달 시 알림 (또는 마지막 항목 교체)
      const msg = currentLang === 'ko' 
        ? `최대 ${maxItems}개까지 순위를 지정할 수 있습니다.` 
        : `You can select up to ${maxItems} items.`;
      alert(msg);
      return;
    }
    rankArray.push(id);
  }
  renderRankBadges(containerId, rankArray);
}

function renderRankBadges(containerId, rankArray) {
  const t = SURVEY_TRANSLATIONS[currentLang];
  const container = document.getElementById(containerId);
  if (!container) return;

  container.querySelectorAll('.rank-item').forEach(item => {
    const id = parseInt(item.getAttribute('data-id'), 10);
    const rankPos = rankArray.indexOf(id); // 0=1순위, 1=2순위, 2=3순위
    const badge = item.querySelector('.rank-badge');

    if (rankPos >= 0) {
      item.classList.add('ranked');
      badge.style.display = 'inline-block';
      badge.className = `rank-badge rank-${rankPos + 1}`;
      badge.textContent = rankPos === 0 ? t.rank_label_1 : (rankPos === 1 ? t.rank_label_2 : t.rank_label_3);
    } else {
      item.classList.remove('ranked');
      badge.style.display = 'none';
      badge.className = 'rank-badge';
      badge.textContent = '';
    }
  });
}

function getMultiSelectValues(containerSelector) {
  const selected = [];
  document.querySelectorAll(`${containerSelector} .choice-item.selected`).forEach(el => {
    selected.push(el.getAttribute('data-id'));
  });
  return selected;
}

function getRadioValue(name) {
  const checked = document.querySelector(`input[name="${name}"]:checked`);
  return checked ? parseInt(checked.value, 10) : null;
}

async function handleFormSubmit(e) {
  e.preventDefault();

  const country = document.getElementById('country').value.trim();

  if (!country) {
    alert(SURVEY_TRANSLATIONS[currentLang].validation_req);
    return;
  }

  const payload = {
    lang: currentLang,
    company_name: "",
    country: country,
    q1_overall: getRadioValue('q1_overall'),

    // 1. IKS 컨퍼런스
    conf_q1: getRadioValue('conf_q1'),
    conf_q2: getMultiSelectValues('#conf_q2_choices'),
    conf_q3_rank1: confQ3Ranks[0] || null,
    conf_q3_rank2: confQ3Ranks[1] || null,
    conf_q3_rank3: confQ3Ranks[2] || null,
    conf_q3_other: document.getElementById('conf_q3_other') ? document.getElementById('conf_q3_other').value.trim() : null,
    conf_q4: document.getElementById('conf_q4') ? document.getElementById('conf_q4').value.trim() : null,

    // 2. 지자체 IR
    reg_q1: getRadioValue('reg_q1'),
    reg_q2: getRadioValue('reg_q2'),
    reg_q3_rank1: regQ3Ranks[0] || null,
    reg_q3_rank2: regQ3Ranks[1] || null,
    reg_q3_other: document.getElementById('reg_q3_other') ? document.getElementById('reg_q3_other').value.trim() : null,

    // 3. 외투환경 세미나
    semi_q1: getRadioValue('semi_q1'),
    semi_q2: getMultiSelectValues('#semi_q2_choices'),
    semi_q3: document.getElementById('semi_q3') ? document.getElementById('semi_q3').value.trim() : null,

    // 4. M.AX 에너지
    max_q1: getRadioValue('max_q1'),
    max_q2: getMultiSelectValues('#max_q2_choices'),
    max_q3: document.getElementById('max_q3') ? document.getElementById('max_q3').value.trim() : null,

    // 5. VC 포럼
    vc_q1: getRadioValue('vc_q1'),
    vc_q2: getMultiSelectValues('#vc_q2_choices'),
    vc_q3: document.getElementById('vc_q3') ? document.getElementById('vc_q3').value.trim() : null,

    // 6. [신규] 재무적 투자포럼
    fin_q1: getRadioValue('fin_q1'),
    fin_q2: getMultiSelectValues('#fin_q2_choices'),
    fin_q3: document.getElementById('fin_q3') ? document.getElementById('fin_q3').value.trim() : null,

    // 7. 효과 및 성과
    eff_q1: getRadioValue('eff_q1'),
    eff_q2: getRadioValue('eff_q2'),
    eff_q3: getRadioValue('eff_q3')
  };

  const btnSubmit = document.getElementById('btnSubmit');
  const btnText = document.getElementById('btnSubmitText');
  const spinner = document.getElementById('submitSpinner');

  btnSubmit.disabled = true;
  spinner.style.display = 'inline-block';
  btnText.textContent = SURVEY_TRANSLATIONS[currentLang].btn_submitting;

  try {
    const response = await fetch('/api/survey/submit', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.detail || '제출에 실패했습니다.');
    }

    // 성공 화면으로 전환
    document.getElementById('iksSurveyForm').style.display = 'none';
    const successCard = document.getElementById('successCard');
    successCard.style.display = 'block';
    window.scrollTo({ top: 0, behavior: 'smooth' });

  } catch (err) {
    console.error('Submission error:', err);
    alert(err.message || '네트워크 오류가 발생했습니다. 잠시 후 다시 시도해주세요.');
  } finally {
    btnSubmit.disabled = false;
    spinner.style.display = 'none';
    btnText.textContent = SURVEY_TRANSLATIONS[currentLang].btn_submit;
  }
}

