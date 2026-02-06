# Saramin Talent Search - AI Instruction Manual

This document serves as a standard operating procedure (SOP) for the AI Agent to perform talent search on **Saramin**.

> [!IMPORTANT]
> **Operational Constraint**: All actions must be performed using the **Browser Tool** only. Do NOT create or use external scripts (Python/Selenium, etc).
>
> [!CRITICAL]
> **Tab Management**: Always ensure you are interacting with the **ACTIVE** browser tab. Multiple tabs with the same URL may exist.
> - Check metadata for `[ACTIVE]` indicator (e.g., `Page ... [ACTIVE]`).
> - Interacting with background tabs will result in silent failures (actions technically succeed but user sees nothing).
>
> [!CRITICAL]
> [!CRITICAL]
> **Korean Input Protocol (Robust)**: Standard JS value setting often fails to trigger tag creation.
> - **Proven Method**:
>   1. **Focus**: Click the input field to ensure focus.
>   2. **Paste**: Use `document.execCommand('insertText', false, 'keyword')`. This mimics user pasting and is more reliable than direct value assignment.
>   3. **Enter**: Press the physical 'Enter' key (or simulate it perfectly).
> - **Verification**: Always check if a **Tag** (e.g., `<span class="tag">keyword</span>`) is created before clicking Search.

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

### Step 2: Talent Search Protocol (Standardized)

1.  **Reset & Open Layer**:
    - Click "초기화" (Reset) button.
    - Click the search input area (placeholder: '직무, 스킬, 회사 등') to **Open the Search Layer**.

2.  **Configuration (Exact Match)**:
    - Locate **'키워드 일치 검색' (Exact Match)** option.
    - **Toggle ON**: Ensure the checkbox is checked. (Click label if unchecked).

3.  **Input Keywords (Protocol)**:
    - **Main (OR) Input**:
        - Target: First input box (`.search_input`).
        - Usage: Primary keywords (e.g., "금융") with **Exact Match**.
        - Action: Focus -> `execCommand` -> Enter.
    - **AND (Include) Input**:
        - Target: Second input box (Placeholder: "키워드를 모두 포함").
        - Usage: specific constraints (e.g., "보험").
        - Action: Focus -> `execCommand` -> Enter.

    > [!IMPORTANT]
    > **Non-Destructive Refinement**: When adding AND/NOT conditions or filters to an active search, **DO NOT CLICK RESET (초기화)**. Just add the new condition and click Search. Use Reset only when starting a completely unrelated search topic.

4.  **Final Execution**:
    - **Search**: Click the main **Search Button** (`.btn_search`) to finalize.

### Step 3: Extraction

1.  Extract **Top 10 Candidates**.
2.  Fields: Name, Title, Experience, Resume Link.

## 4. Output

- **Path**: `talent-search/candidate/saramin/candidate_list_{Date}_saramin.csv`
