# Saramin Talent Search - AI Instruction Manual

This document serves as a standard operating procedure (SOP) for the AI Agent to perform talent search on **Saramin**.

> [!IMPORTANT]
> **Operational Constraint**: All actions must be performed using the **Browser Tool** only. Do NOT create or use external scripts (Python/Selenium, etc).
>
> [!CRITICAL]
> **Tab Management**: Always ensure you are interacting with the **ACTIVE** browser tab. Multiple tabs with the same URL may exist.
> - Check metadata for `[ACTIVE]` indicator (e.g., `Page ... [ACTIVE]`).
> - Interacting with background tabs will result in silent failures (actions technically succeed but user sees nothing).

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
5.  **Navigate directly to Talent Search Page**:
    - URL: `https://www.saramin.co.kr/zf_user/memcom/talent-pool/main/search`

### Step 2: Talent Search Protocol (Verified)

1.  **Reset Conditions**:
    - Click "초기화" (Reset) button on the right side of the search bar.
    - Wait for reset.

2.  **Base Search (Keyword 'SQA')**:
    - Click `.search_default input.search_input` to open the Search Layer.
    - **Exact Match**: Verify `#keywordSearch` checkbox is CHECKED. If not, click it.
    - **Input Keyword**: 'SQA' -> Press Enter.

3.  **Refine Search (Hangul Input - '개발')**:
    - **Reset Conditions** (Again, if starting fresh test).
    - Open Search Layer.
    - **Exact Match**: Ensure checked.
    - **Input Hangul (JS Injection Required)**:
      - Locate active input element.
      - Use React-compatible setter to input '개발'.
      - Trigger `input` and `change` events.
    - **Search**: Press Enter.
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
