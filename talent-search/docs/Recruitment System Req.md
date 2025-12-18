# AI-Powered Recruitment System
## 요구사항 정의서 및 목표 기술 아키텍처

**Version:** 1.0  
**Date:** 2025-12-18  
**Scope:** 채용 업무 Full Lifecycle AI 자동화

---

## Executive Summary

채용(Recruitment) 업무는 단순 "인재 서칭"을 넘어 **8개 핵심 단계**로 구성된 End-to-End 프로세스입니다. 본 문서는 각 단계를 AI로 자동화/지원하기 위한 요구사항과 기술 스택을 정의합니다.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        RECRUITMENT LIFECYCLE                                │
├─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬──────┤
│ Planning│ Sourcing│Screening│ Assess  │Interview│ Offer   │Onboard  │Report│
│    1    │    2    │    3    │    4    │    5    │    6    │    7    │   8  │
└─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴──────┘
```

---

## Module 1: Workforce Planning & Requisition (인력 계획 및 채용 요청)

### 1.1 Business Requirements

| ID | 요구사항 | 우선순위 |
|----|----------|----------|
| WP-001 | 현업 부서가 자연어로 인력 요청 시 AI가 JD(Job Description) 초안 자동 생성 | P0 |
| WP-002 | 과거 채용 데이터 기반 예상 채용 기간(Time-to-Hire) 예측 | P1 |
| WP-003 | 유사 포지션 JD 추천 및 재사용 지원 | P1 |
| WP-004 | 시장 연봉 데이터 기반 적정 연봉 범위 제안 | P2 |

### 1.2 Functional Specifications

```yaml
JD_Generator:
  input:
    - natural_language_request: "백엔드 개발자 3년차 이상, Java/Spring 필수"
    - department: string
    - headcount: int
  process:
    - NLP로 핵심 요구사항 추출 (role, experience, skills, domain)
    - 내부 JD 템플릿 DB에서 유사 JD 검색
    - LLM으로 JD 초안 생성 (responsibilities, qualifications, preferred)
    - 법적 필수 문구 자동 삽입 (차별금지 조항 등)
  output:
    - draft_jd: markdown/docx
    - similar_jds: list[JD]
    - estimated_time_to_hire: int (days)
    - suggested_salary_range: {min, max, median}
```

### 1.3 Target Tech Stack

| Component | Technology | Rationale |
|-----------|------------|-----------|
| LLM | Claude API / GPT-4 | JD 생성, 자연어 이해 |
| Vector DB | Pinecone / Chroma | 유사 JD 검색 (Semantic Search) |
| Backend | FastAPI / Python | 빠른 프로토타이핑 |
| Storage | PostgreSQL + S3 | JD 메타데이터 + 파일 저장 |

---

## Module 2: Job Posting & Talent Sourcing (공고 및 인재 서칭)

> ⚠️ 기존 프로젝트 문서가 다루는 범위 + 확장

### 2.1 Business Requirements

| ID | 요구사항 | 우선순위 |
|----|----------|----------|
| JS-001 | 자연어 기반 인재 검색 (멀티 사이트: JobKorea, Saramin, LinkedIn 등) | P0 |
| JS-002 | 검색어/필터 조합 자동 최적화 | P0 |
| JS-003 | JD → 복수 채용 플랫폼 동시 게시 (Cross-posting) | P1 |
| JS-004 | 플랫폼별 공고 성과(조회수, 지원율) 추적 | P1 |
| JS-005 | Passive Candidate 발굴 (GitHub, LinkedIn 프로필 분석) | P2 |

### 2.2 Functional Specifications

```yaml
TalentSearchEngine:
  input:
    - query: "금융권 10년차 이상 QA 팀장급"
    - platforms: [jobkorea, saramin, linkedin]
    - constraints:
        location: "서울"
        salary_range: optional
  process:
    - Query Understanding: LLM이 의도 분석 → structured query 변환
    - Query Expansion: 동의어/유사 직무 자동 확장
        - "QA" → ["QA", "Quality Assurance", "테스터", "품질관리"]
    - Multi-platform Search: 각 플랫폼 API/Scraper 병렬 실행
    - Deduplication: 동일인 cross-platform 매칭 (이름+경력 해싱)
    - Ranking: 적합도 점수 기반 정렬
  output:
    - candidates: list[CandidateProfile]
    - search_metadata: {platforms_searched, total_results, query_variations}
```

```yaml
JobPostingManager:
  input:
    - jd: JobDescription
    - target_platforms: list[Platform]
    - posting_schedule: optional[datetime]
  process:
    - Platform Adapter: 각 플랫폼 포맷으로 JD 변환
    - Compliance Check: 플랫폼별 금지어/필수요소 검증
    - Scheduled Posting: 지정 시간 자동 게시
    - Performance Tracking: 조회수, 지원수 주기적 수집
  output:
    - posting_urls: dict[platform, url]
    - performance_report: periodic
```

### 2.3 Target Tech Stack

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Browser Automation | Playwright (Python) | 동적 사이트 대응, 안정성 |
| Anti-Detection | playwright-stealth | 봇 탐지 우회 |
| Task Queue | Celery + Redis | 비동기 멀티 플랫폼 크롤링 |
| Proxy | Residential Proxy Pool | IP 차단 방지 |
| NLP | spaCy + Custom NER | 이력서 엔티티 추출 |

---

## Module 3: Resume Screening & Shortlisting (서류 심사 및 후보자 선별)

### 3.1 Business Requirements

| ID | 요구사항 | 우선순위 |
|----|----------|----------|
| RS-001 | 이력서 자동 파싱 (PDF, DOCX, HWP 지원) | P0 |
| RS-002 | JD 기준 적합도 점수(Fit Score) 자동 산출 | P0 |
| RS-003 | 불합격 사유 자동 생성 (내부 기록용) | P1 |
| RS-004 | Bias Detection: 성별/나이/학력 편향 경고 | P1 |
| RS-005 | 후보자 요약 카드 자동 생성 | P0 |

### 3.2 Functional Specifications

```yaml
ResumeParser:
  input:
    - file: binary (pdf/docx/hwp)
  process:
    - Format Detection & Conversion (hwp → pdf → text)
    - Section Segmentation: 학력, 경력, 스킬, 자격증, 프로젝트
    - Entity Extraction:
        - companies: list[{name, period, role}]
        - skills: list[str]
        - education: list[{school, degree, major, year}]
        - certifications: list[str]
    - Normalization: 회사명/학교명 표준화 (삼성전자/삼성 → Samsung Electronics)
  output:
    - structured_resume: JSON
    - raw_text: str
    - confidence_score: float
```

```yaml
FitScoreCalculator:
  input:
    - resume: StructuredResume
    - jd: JobDescription
  process:
    - Requirement Matching:
        - Must-have 스킬 매칭률
        - 경력 연차 적합성
        - 도메인 경험 매칭
    - Soft Signal Analysis:
        - 이직 빈도 (Job Hopping Risk)
        - 경력 성장 트렌드
        - 회사 규모/문화 fit
    - LLM Summary: 강점/약점 2-3줄 요약
  output:
    - fit_score: 0-100
    - breakdown: {skills: 85, experience: 70, domain: 90}
    - summary: str
    - red_flags: list[str]
    - bias_warning: optional[str]  # "나이 기반 필터 감지됨"
```

### 3.3 Target Tech Stack

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Resume Parser | LlamaParse / Unstructured.io | 복잡한 레이아웃 처리 |
| HWP Support | hwp5 / LibreOffice | 한국 특수 포맷 |
| Embedding | OpenAI text-embedding-3 | 시맨틱 유사도 계산 |
| Scoring | Custom ML Model + LLM | 규칙 기반 + AI 하이브리드 |
| Bias Detection | Fairlearn / Custom Rules | 공정성 감사 |

---

## Module 4: Assessment & Evaluation (역량 평가)

### 4.1 Business Requirements

| ID | 요구사항 | 우선순위 |
|----|----------|----------|
| AE-001 | 직무별 맞춤 코딩 테스트 자동 출제 | P1 |
| AE-002 | 코딩 테스트 자동 채점 + 코드 품질 분석 | P1 |
| AE-003 | 사전 과제 평가 기준 생성 및 AI 보조 채점 | P2 |
| AE-004 | 인적성 검사 결과 요약 | P2 |

### 4.2 Functional Specifications

```yaml
CodingTestGenerator:
  input:
    - role: "Backend Developer"
    - level: "Senior (5+ years)"
    - tech_stack: ["Java", "Spring", "MySQL"]
    - difficulty: "Medium-Hard"
  process:
    - 문제 은행에서 적합한 문제 선별
    - 난이도/주제 밸런싱
    - 회사별 커스텀 시나리오 적용 가능
  output:
    - test_set: list[Problem]
    - estimated_duration: int (minutes)
    - evaluation_rubric: dict

CodingTestEvaluator:
  input:
    - submission: code
    - problem: Problem
    - rubric: EvaluationRubric
  process:
    - Correctness: 테스트 케이스 통과율
    - Performance: 시간/공간 복잡도 분석
    - Code Quality: 
        - 가독성 (naming, structure)
        - 베스트 프랙티스 준수
        - 보안 취약점 체크
    - LLM Review: 코드 리뷰 코멘트 생성
  output:
    - score: 0-100
    - breakdown: {correctness, performance, quality}
    - detailed_feedback: str
    - code_review_comments: list[Comment]
```

### 4.3 Target Tech Stack

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Code Execution | Judge0 / Piston | 안전한 샌드박스 실행 |
| Static Analysis | SonarQube API / semgrep | 코드 품질 분석 |
| Problem Bank | Custom DB + LeetCode-style | 문제 관리 |
| AI Review | Claude Code / GPT-4 | 코드 리뷰 자동화 |

---

## Module 5: Interview Management (면접 관리)

### 5.1 Business Requirements

| ID | 요구사항 | 우선순위 |
|----|----------|----------|
| IM-001 | 면접관/후보자 일정 자동 조율 (Calendar Integration) | P0 |
| IM-002 | 이력서 기반 맞춤 면접 질문 자동 생성 | P0 |
| IM-003 | 면접 피드백 수집 및 구조화 | P1 |
| IM-004 | 면접 결과 종합 리포트 자동 생성 | P1 |
| IM-005 | 화상 면접 녹화본 요약 (STT + Summarization) | P2 |

### 5.2 Functional Specifications

```yaml
InterviewScheduler:
  input:
    - candidate: Candidate
    - interviewers: list[Employee]
    - duration: int (minutes)
    - deadline: date
    - interview_type: ["phone", "video", "onsite"]
  process:
    - Calendar API로 각 참석자 가용 시간 조회
    - 최적 슬롯 계산 (선호 시간대 가중치 적용)
    - 후보자에게 시간 선택 옵션 제공 (2-3개)
    - 확정 시 캘린더 이벤트 자동 생성
    - 면접 전 리마인더 발송
  output:
    - scheduled_interview: InterviewEvent
    - calendar_invites: sent
    - reminder_scheduled: true

InterviewQuestionGenerator:
  input:
    - resume: StructuredResume
    - jd: JobDescription
    - interview_stage: ["1차 기술면접", "2차 임원면접", "컬처핏"]
  process:
    - Resume Gap Analysis: 확인 필요 사항 도출
    - Role-specific Questions: 직무별 기술 질문
    - Behavioral Questions: STAR 기반 역량 질문
    - Culture Fit Questions: 회사 가치관 기반
    - Red Flag Probing: 이력서 의심 구간 검증 질문
  output:
    - question_set: list[Question]
    - question_intent: dict[question, purpose]
    - follow_up_suggestions: list[str]

InterviewFeedbackAggregator:
  input:
    - feedbacks: list[InterviewerFeedback]
    - scoring_rubric: ScoringRubric
  process:
    - 점수 정규화 (면접관별 편차 보정)
    - 의견 불일치 구간 하이라이트
    - 종합 평가 생성
  output:
    - aggregated_score: float
    - consensus_summary: str
    - disagreement_areas: list[str]
    - hiring_recommendation: ["Strong Yes", "Yes", "Maybe", "No", "Strong No"]
```

### 5.3 Target Tech Stack

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Calendar | Google Calendar API / MS Graph | 기업 캘린더 연동 |
| Scheduling | Cal.com / Calendly API | 외부 후보자 셀프 예약 |
| Video Interview | Zoom API / Google Meet | 화상 면접 관리 |
| STT | Whisper / Clova Speech | 면접 녹취록 생성 |
| Summarization | Claude / GPT-4 | 면접 내용 요약 |

---

## Module 6: Offer Management (오퍼 관리)

### 6.1 Business Requirements

| ID | 요구사항 | 우선순위 |
|----|----------|----------|
| OM-001 | 내부 연봉 테이블 + 시장 데이터 기반 오퍼 금액 추천 | P1 |
| OM-002 | 오퍼 레터 자동 생성 (템플릿 기반) | P1 |
| OM-003 | 협상 시나리오별 대응 가이드 제공 | P2 |
| OM-004 | 오퍼 수락/거절 추적 및 분석 | P1 |

### 6.2 Functional Specifications

```yaml
OfferRecommender:
  input:
    - candidate: Candidate
    - position: Position
    - internal_salary_band: SalaryBand
    - market_data: MarketSalaryData
    - negotiation_room: float  # 협상 여유분 (%)
  process:
    - 후보자 현재 연봉 대비 적정 인상률 계산
    - 내부 형평성 체크 (동일 레벨 기존 직원 대비)
    - 시장 데이터 대비 경쟁력 분석
    - 최종 추천 범위 산출
  output:
    - recommended_base: {min, target, max}
    - signing_bonus_suggestion: optional[int]
    - equity_suggestion: optional[str]
    - justification: str
    - internal_equity_flag: optional[str]

OfferLetterGenerator:
  input:
    - candidate: Candidate
    - offer_details: OfferDetails
    - template: OfferTemplate
  process:
    - 템플릿 변수 치환
    - 법적 필수 조항 검증
    - PDF 생성 + 전자서명 링크 포함
  output:
    - offer_letter: PDF
    - e_sign_link: url
```

### 6.3 Target Tech Stack

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Document Gen | docx-js / WeasyPrint | 오퍼 레터 생성 |
| E-Signature | DocuSign API / 모두싸인 | 전자서명 |
| Salary Data | Wanted 연봉 API / Glassdoor | 시장 데이터 |

---

## Module 7: Pre-boarding & Onboarding (입사 준비 및 온보딩)

### 7.1 Business Requirements

| ID | 요구사항 | 우선순위 |
|----|----------|----------|
| OB-001 | 입사 서류 체크리스트 자동 발송 및 추적 | P1 |
| OB-002 | IT 장비/계정 신청 자동화 (연동) | P1 |
| OB-003 | 신규 입사자 맞춤 온보딩 플랜 생성 | P2 |
| OB-004 | 온보딩 진행 상황 대시보드 | P2 |
| OB-005 | 신규 입사자 FAQ 챗봇 | P2 |

### 7.2 Functional Specifications

```yaml
PreboardingOrchestrator:
  input:
    - new_hire: Employee
    - start_date: date
    - position: Position
  process:
    - D-14: 입사 서류 요청 메일 발송
    - D-7: 서류 제출 리마인더
    - D-5: IT 장비/계정 신청 (ITSM 연동)
    - D-3: 좌석 배정 확인
    - D-1: 웰컴 키트 발송 확인
    - D-Day: 온보딩 스케줄 안내
  output:
    - preboarding_status: ChecklistStatus
    - blockers: list[str]

OnboardingPlanGenerator:
  input:
    - new_hire: Employee
    - role: Role
    - team: Team
  process:
    - 직무별 필수 교육 과정 매핑
    - 팀별 온보딩 버디 자동 매칭
    - 30-60-90일 목표 제안
    - 주요 이해관계자 미팅 일정 추천
  output:
    - onboarding_plan: OnboardingPlan
    - buddy_assignment: Employee
    - milestone_goals: list[Goal]
```

### 7.3 Target Tech Stack

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Workflow | n8n / Temporal | 복잡한 프리보딩 워크플로우 |
| ITSM Integration | ServiceNow API / Jira SM | IT 자동화 |
| Chatbot | Claude + RAG | 신규 입사자 FAQ |
| Notification | Slack API / Email | 알림 발송 |

---

## Module 8: Analytics & Reporting (분석 및 리포팅)

### 8.1 Business Requirements

| ID | 요구사항 | 우선순위 |
|----|----------|----------|
| AR-001 | 실시간 채용 파이프라인 대시보드 | P0 |
| AR-002 | 주요 KPI 자동 계산 (Time-to-Hire, Cost-per-Hire 등) | P0 |
| AR-003 | 채용 병목 구간 자동 탐지 | P1 |
| AR-004 | 월간/분기 채용 리포트 자동 생성 | P1 |
| AR-005 | 채용 트렌드 예측 (ML 기반) | P2 |

### 8.2 Key Metrics Definitions

```yaml
Metrics:
  Time_to_Hire:
    definition: "공고 게시일 ~ 오퍼 수락일"
    target: "< 30 days"
    
  Time_to_Fill:
    definition: "채용 요청일 ~ 입사일"
    target: "< 45 days"
    
  Cost_per_Hire:
    definition: "(Internal Costs + External Costs) / Total Hires"
    components:
      - recruiter_salary_allocated
      - job_board_fees
      - agency_fees
      - referral_bonuses
      
  Source_of_Hire:
    definition: "채용 채널별 합격자 비율"
    channels: [jobkorea, saramin, linkedin, referral, direct, agency]
    
  Offer_Acceptance_Rate:
    definition: "오퍼 수락 / 오퍼 발송"
    target: "> 85%"
    
  Quality_of_Hire:
    definition: "신규 입사자 1년 내 성과 평가 + 재직률"
    measurement_period: "12 months"
    
  Funnel_Conversion:
    stages:
      - applied → screened
      - screened → interviewed  
      - interviewed → offered
      - offered → hired
```

### 8.3 Functional Specifications

```yaml
RecruitmentDashboard:
  views:
    - Pipeline View: 단계별 후보자 현황
    - Funnel View: 전환율 시각화
    - Time Series: 월별 채용 추이
    - Source Analysis: 채널별 효율성
    - Bottleneck Alert: 병목 구간 하이라이트
    
  filters:
    - date_range
    - department
    - position_level
    - recruiter
    
  export:
    - PDF Report
    - Excel Raw Data
    - Scheduled Email

AutoReportGenerator:
  input:
    - report_type: ["weekly", "monthly", "quarterly"]
    - scope: Department | Company
  process:
    - 기간 내 데이터 집계
    - YoY/MoM 비교
    - 주요 인사이트 자동 추출 (LLM)
    - 차트 자동 생성
  output:
    - report: PDF/PPTX
    - executive_summary: str (3-5 bullet points)
```

### 8.4 Target Tech Stack

| Component | Technology | Rationale |
|-----------|------------|-----------|
| BI Dashboard | Metabase / Apache Superset | 오픈소스, 셀프 호스팅 |
| Data Warehouse | PostgreSQL / BigQuery | 분석용 데이터 저장 |
| ETL | dbt / Airflow | 데이터 파이프라인 |
| Visualization | Plotly / Chart.js | 커스텀 차트 |
| Report Gen | WeasyPrint + Jinja2 | PDF 리포트 |

---

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              PRESENTATION LAYER                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  Web App (React)  │  Slack Bot  │  Email Integration  │  Mobile App (RN)   │
└────────┬──────────┴──────┬──────┴─────────┬───────────┴─────────┬──────────┘
         │                 │                │                     │
         ▼                 ▼                ▼                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                API GATEWAY                                   │
│                        (Kong / AWS API Gateway)                              │
└────────┬────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                             SERVICE LAYER                                    │
├─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬──────┤
│Planning │Sourcing │Screening│  Assess │Interview│  Offer  │Onboard  │Report│
│ Service │ Service │ Service │ Service │ Service │ Service │ Service │ Svc  │
└────┬────┴────┬────┴────┬────┴────┬────┴────┬────┴────┬────┴────┬────┴──┬───┘
     │         │         │         │         │         │         │       │
     ▼         ▼         ▼         ▼         ▼         ▼         ▼       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            SHARED SERVICES                                   │
├──────────────┬──────────────┬──────────────┬──────────────┬─────────────────┤
│   AI/LLM     │   Document   │ Notification │   Calendar   │  Integration    │
│   Gateway    │   Service    │   Service    │   Service    │    Hub          │
│ (Claude/GPT) │ (Parse/Gen)  │ (Email/Slack)│ (GCal/O365)  │ (JobKorea etc)  │
└──────────────┴──────────────┴──────────────┴──────────────┴─────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATA LAYER                                      │
├──────────────────┬──────────────────┬───────────────────┬───────────────────┤
│   PostgreSQL     │    Vector DB     │      Redis        │       S3          │
│   (Main DB)      │   (Embeddings)   │    (Cache/Queue)  │   (Files/Docs)    │
└──────────────────┴──────────────────┴───────────────────┴───────────────────┘
```

---

## Data Model (Core Entities)

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│   Requisition   │       │    Candidate    │       │   Application   │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ id              │       │ id              │       │ id              │
│ title           │       │ name            │       │ requisition_id  │──┐
│ department_id   │──┐    │ email           │       │ candidate_id    │──┼─┐
│ jd_content      │  │    │ phone           │       │ stage           │  │ │
│ status          │  │    │ resume_url      │       │ fit_score       │  │ │
│ headcount       │  │    │ structured_data │       │ source          │  │ │
│ salary_range    │  │    │ created_at      │       │ created_at      │  │ │
│ created_at      │  │    └────────┬────────┘       └─────────────────┘  │ │
└─────────────────┘  │             │                                      │ │
                     │             │    ┌─────────────────────────────────┘ │
                     │             │    │                                   │
                     ▼             ▼    ▼                                   │
              ┌─────────────────────────────┐       ┌─────────────────┐     │
              │       Interview             │       │    Assessment   │     │
              ├─────────────────────────────┤       ├─────────────────┤     │
              │ id                          │       │ id              │     │
              │ application_id              │──┐    │ application_id  │─────┘
              │ interviewer_ids             │  │    │ type            │
              │ scheduled_at                │  │    │ score           │
              │ feedback                    │  │    │ result_data     │
              │ recommendation              │  │    │ evaluated_at    │
              └─────────────────────────────┘  │    └─────────────────┘
                                               │
                                               ▼
                                        ┌─────────────────┐
                                        │     Offer       │
                                        ├─────────────────┤
                                        │ id              │
                                        │ application_id  │
                                        │ salary          │
                                        │ status          │
                                        │ sent_at         │
                                        │ responded_at    │
                                        └─────────────────┘
```

---

## Implementation Roadmap

### Phase 1: Foundation (Month 1-2)
- [ ] Core DB Schema & API 설계
- [ ] 인증/권한 시스템 (RBAC)
- [ ] Module 2: Sourcing MVP (단일 플랫폼)
- [ ] Module 3: Resume Parser MVP

### Phase 2: Core Features (Month 3-4)
- [ ] Module 2: Multi-platform Sourcing
- [ ] Module 3: Fit Score Calculator
- [ ] Module 5: Interview Scheduling
- [ ] Module 8: Basic Dashboard

### Phase 3: Advanced AI (Month 5-6)
- [ ] Module 1: JD Generator
- [ ] Module 5: Question Generator
- [ ] Module 4: Coding Test MVP
- [ ] 자연어 인터페이스 (Slack/Chat)

### Phase 4: Full Automation (Month 7-8)
- [ ] Module 6: Offer Management
- [ ] Module 7: Onboarding Automation
- [ ] Module 8: Auto Report Generation
- [ ] End-to-End Integration Testing

---

## Risk & Considerations

| Risk | Impact | Mitigation |
|------|--------|------------|
| 채용 사이트 크롤링 차단 | High | Rate limiting, Proxy rotation, 공식 API 우선 사용 |
| 개인정보 보호법 위반 | Critical | 동의 기반 수집, 암호화, 보관 기간 준수 |
| AI 편향 (Bias) | High | Fairness audit, Human-in-the-loop |
| LLM 비용 | Medium | 캐싱, 경량 모델 혼용, 배치 처리 |
| 기존 ATS 연동 | Medium | 표준 API, 데이터 마이그레이션 플랜 |

---

## Appendix: Glossary

| Term | Definition |
|------|------------|
| ATS | Applicant Tracking System - 지원자 추적 시스템 |
| JD | Job Description - 직무 기술서 |
| Requisition | 채용 요청서 |
| Sourcing | 인재 발굴/서칭 |
| Screening | 서류 심사 |
| Fit Score | 직무 적합도 점수 |
| Time-to-Hire | 공고~오퍼수락 소요 기간 |
| RAG | Retrieval Augmented Generation |

---

*Document Version: 1.0*  
*Last Updated: 2025-12-18*