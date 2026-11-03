# 2026 Invest KOREA Summit (IKS) 참가자 설문조사 시스템

2026 Invest KOREA Summit 현장에서 스마트폰 QR 코드로 접속해 응답할 수 있는 모바일 최적화 다국어(국문/영문) 설문조사 웹 서비스 및 관리자 통계/엑셀 다운로드 시스템입니다.

---

## 🌟 주요 특징

1. **원천 설문 완벽 반영 (국문 / 영문)**
   - `IKS2026_만족도_설문조사_국문(1103).hwp` 및 `IKS_2026_Participant_Survey_EN.docx` 파일 내용을 파싱하여 국문/영문 설문 데이터 구조 일치
   - 기본 정보(기업명, 국가), 총괄 만족도, 5개 핵심 세션(컨퍼런스, 지자체IR, 외투환경 세미나, M.AX에너지 포럼, 글로벌VC 스타트업 포럼) 전체 구현
   - 상단 언어 전환 토글(한국어 ↔ English) 클릭 시 실시간 다국어 렌더링 (작성 중인 응답 데이터 보존)

2. **동시 접속 300+명 지원 고성능 비동기 아키텍처**
   - **FastAPI (ASGI)**: 고성능 비동기 이벤트 루프 기반 논블로킹 요청 처리
   - **SQLite WAL 모드 (Write-Ahead Logging)**: 읽기/쓰기 동시 락 경합 해소
   - `busy_timeout=10,000ms`, `synchronous=NORMAL`, 64MB 메모리 캐시 최적화 적용으로 수백 명의 동시 설문 제출 안전 처리

3. **모바일 QR 최적화 UX**
   - 모바일 터치 친화적 5점 리커트 척도 버튼
   - 터치 인터랙션 기반 순위 선택 (최대 3순위/2순위 지정 시 배지 즉시 부여 및 재클릭 시 자동 재정렬)
   - 모바일 가독성을 고려한 반응형 카드 레이아웃 & 로딩 피드백

4. **관리자 센터 & 엑셀(.xlsx) 원클릭 다운로드 API**
   - 엔드포인트: `/api/admin/export`
   - **pandas + openpyxl** 기반 3개 전문 시트 구성:
     - `설문응답_상세`: 문항별 국문/영문 실제 응답 텍스트 매핑, 헤더 네이비 스타일링, 열 너비 자동 맞춤
     - `만족도통계_요약`: 전체 응답자 수, 국/영문 비율, 세션별 평균 점수(5점 만점) 요약
     - `원천수치데이터_SPSS용`: SPSS / R 통계 분석용 1~5점 수치 코드 데이터
   - 관리자 대시보드 (`/admin`): 실시간 제출 카운트, 세션별 평점 현황, 최근 응답 목록 제공

5. **현장 배포용 고화질 QR 코드 생성기**
   - 행사 현장 Wi-Fi/LAN의 로컬 IPv4 주소를 자동 탐지하여 스마트폰에서 바로 접속 가능한 안내 배너 포함 PNG 이미지 자동 생성 (`scripts/generate_qr.py`)

---

## 📁 프로젝트 구조

```
IKS_survey/
│
├── app/
│   ├── __init__.py
│   ├── config.py           # 환경 설정 (포트, DB경로, 관리자 키)
│   ├── database.py         # SQLite WAL 모드 연결 및 테이블 스키마 초기화
│   ├── models.py           # Pydantic 입력 유효성 검증 모델
│   ├── survey_data.py      # 국문/영문 설문 메타데이터 및 보기 매핑
│   ├── api.py              # 설문 제출 및 관리자 엑셀 다운로드 API
│   └── excel_exporter.py   # 전문 엑셀 리포트(.xlsx) 생성 엔진
│
├── static/
│   ├── css/style.css       # 모바일 반응형 디자인 스타일시트
│   ├── js/survey_content.js# 다국어(국/영문) 전체 텍스트 맵
│   └── js/app.js           # 언어 전환, 순위 선택, 폼 검증 및 제출 로직
│
├── templates/
│   ├── index.html          # 참가자 모바일 설문 웹 페이지
│   └── admin.html          # 관리자 대시보드 및 엑셀 다운로드 웹 페이지
│
├── scripts/
│   ├── generate_qr.py      # 모바일 접속용 QR 코드 PNG 생성 스크립트
│   ├── load_test.py        # 300명 동시 제출 부하 테스트 스크립트
│   └── test_system.py      # 파이프라인 단위 테스트 스크립트
│
├── iks2026_survey_qr.png   # 생성된 QR 코드 이미지 파일
├── requirements.txt        # 의존성 패키지 목록
└── main.py                 # FastAPI 웹 서버 메인 엔트리포인트
```

---

## 🚀 실행 방법

### 1. 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. QR 코드 이미지 생성
```bash
python scripts/generate_qr.py
```
> 현장 로컬 IP(예: `http://192.168.0.x:8000/`)가 자동 적용된 `iks2026_survey_qr.png` 파일이 생성됩니다.

### 3. 웹 서버 실행 (Live)
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

- **참가자 설문 페이지 (QR 타깃)**: `http://localhost:8000/` 또는 `http://<내 로컬 IP>:8000/`
- **관리자 대시보드 & 엑셀 다운로드**: `http://localhost:8000/admin` (기본 인증키: `iks2026admin`)
- **API 문서 (Swagger UI)**: `http://localhost:8000/docs`

### 4. 300인 동시 접속 부하 테스트
```bash
python scripts/load_test.py 300 50
```

