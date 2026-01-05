# Talent Search Automation Project: Background & Vision

**Date:** 2025-12-18
**Context:** HR Team Talent Acquisition Efficiency Improvement

## 1. Problem Statement (배경 및 문제점)
인사팀으로서 현업 부서의 인재 서칭 요청(Talent Sourcing Request)을 수행하는 과정에서 다음과 같은 비효율이 발생하고 있습니다.

*   **High Manual Effort (과도한 수작업):** JobKorea, Saramin 등 채용 포털에 접속하여 수동으로 검색 메뉴를 조작해야 함.
*   **Search Complexity (검색의 어려움):** 단순히 키워드 하나로 끝나는 것이 아니라, 다양한 검색 조건('일치검색' vs '통합검색', 직무 필터 등)을 조합하고 시도해봐야 하는데, 이를 일일이 수행하기 번거로움.
*   **Time-Consuming Review (리뷰 시간 소요):** 검색 결과로 나온 수십, 수백 명의 후보자 프로필을 일일이 클릭하여 상세 이력을 파악하고 적합성을 판단하는 데 막대한 시간이 소요됨.

## 2. Solution Approach (해결 방안)
AI의 도움을 받아 이 과정을 혁신하고자 합니다.

### Phase 1: Guided Learning (AI 학습 및 프로세스 정립) - *Current Stage*
*   AI와 함께 실제 채용 사이트(JobKorea 등)의 UI를 하나씩 점검하고 실습함.
*   AI에게 웹사이트의 구조와 채용 담당자가 실제로 일하는 방식(Workflow)을 설명하고 보여줌으로써, 업무 맥락을 이해시킴.

### Phase 2: Automation (스크립트화 및 자동화)
*   Phase 1에서 파악한 프로세스를 바탕으로 자동화 스크립트(Python, Playwright 등)를 개발함.
*   반복적인 로그인, 검색어 입력, 리스트 추출 작업을 자동화하여 물리적인 시간을 단축함.

### Phase 3: Natural Language Interface (자연어 기반 업무 수행) - *Ultimate Goal*
*   인사팀 담당자가 **자연어(Natural Language)**로 원하는 인재상을 말하면, AI가 이를 이해하여 스스로 수행함.
    *   Example: *"금융권 경력이 있는 10년차 이상의 QA 팀장급을 찾아줘"*
*   **AI의 역할:**
    1.  요청을 분석하여 최적의 검색어(Keywords)와 검색 조건(Filters)을 스스로 생성.
    2.  다양한 조합으로 검색을 시도하여 최상의 결과를 도출.
    3.  검색된 후보자들의 이력서를 읽고 요약하여, 인사팀이 빠르게 의사결정을 내릴 수 있도록 지원.

## 3. Expected Value (기대 효과)
*   **Efficiency:** 단순 반복 작업 제거로 인재 발굴 속도 비약적 향상.
*   **Quality:** 다양한 검색 시나리오를 AI가 대신 수행함으로써 놓칠 수 있는 인재 발굴 가능성 증대.
*   **Usability:** 복잡한 검색 문법을 몰라도 자연어로 쉽게 인재 서칭 가능.
