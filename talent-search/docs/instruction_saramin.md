# Saramin Talent Search - AI Instruction Manual

This document serves as a standard operating procedure (SOP) for the AI Agent to perform talent search on **Saramin**.

## 1. Input Variables

- **Target Keyword**: (e.g., "SQA", "Finance", "Java")
- **Search Date**: (Today's date in YYYY-MM-DD format)

## 2. Pre-requisites

- **Credentials**:
  - ID: `wisewires`
  - PW: `insa5051`
- **Target URL**: `https://www.saramin.co.kr/zf_user/member/companies/login` (Corporate Login)

## 3. Execution Steps (Draft)

### Step 1: Login

1.  Navigate to Saramin Login page: `https://www.saramin.co.kr/zf_user/auth`
2.  **Click "Corporate Member" (기업회원) Tab**:
    - Selector: `.btn_tab.t_com`
3.  Enter Credentials (JS Injection recommended):
    - ID Selector: `#id`
    - PW Selector: `#password`
    - Button Selector: `.btn_login`
4.  Verify successful login (Check URL changes to `hiring.saramin.co.kr`).

### Step 2: Talent Search Protocol (Combined AND)

**Rule 1**: Group all AND keywords in the "AND" field before searching.
**Rule 2** (Autonomous): **Do NOT ask for confirmation.** Execute the search immediately after inputting keywords.

1.  **Base Search (Result Set 1)**:
    - **Focus OR Input**: Click `.search_default input.search_input`.
    - **Enable Exact Match**:
      - Locate Toggle Label: `label[for="keywordSearch"]`
      - Action: Click the **Label** if checkbox `#keywordSearch` is not checked.
    - **Input Keyword**: "SQA" -> Press Enter or Click Search (`.btn_search`).
2.  **Refine Search (AND Conditions)**:
    - **Locate AND Input**: `.search_word_include input.search_input` (Placeholder: 키워드를 모두 포함)
    - **Input Keywords**:
      - "금융" (Enter/Chip).
      - "개발" (Enter/Chip).
    - **Click SEARCH**: Trigger search again.
3.  **Filters**: Apply filters (Experience 5yr+) after keywords.

### Step 3: Extraction

1.  Extract **Top 10 Candidates**.
2.  Fields: Name, Title, Experience, Resume Link.

## 4. Output

- **Path**: `talent-search/candidate/saramin/candidate_list_{Date}_saramin.csv`
