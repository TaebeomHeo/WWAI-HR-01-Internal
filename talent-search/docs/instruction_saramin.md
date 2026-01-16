# Saramin Talent Search - AI Instruction Manual

This document serves as a standard operating procedure (SOP) for the AI Agent to perform talent search on **Saramin**.

## 1. Input Variables
*   **Target Keyword**: (e.g., "SQA", "Finance", "Java")
*   **Search Date**: (Today's date in YYYY-MM-DD format)

## 2. Pre-requisites
*   **Credentials**:
    *   ID: `wisewires`
    *   PW: `insa5051`
*   **Target URL**: `https://www.saramin.co.kr/zf_user/member/companies/login` (Corporate Login)

## 3. Execution Steps (Draft)

### Step 1: Login
1.  Navigate to Saramin Corporate Login page.
2.  Enter ID and PW.
3.  Verify successful login.

### Step 2: Talent Search Protocol (Combined AND)
**Rule 1**: Group all AND keywords in the "AND" field before searching.
**Rule 2** (Autonomous): **Do NOT ask for confirmation.** Execute the search immediately after inputting keywords.

1.  **Base Search (Result Set 1)**:
    *   Input **"SQA"** (Exact Match) -> Click **Search**.
2.  **Refine Search (AND Conditions)**:
    *   Locate **"AND 키워드를 모두 포함"** field.
    *   Input **"금융"** (Enter/Chip).
    *   Input **"개발"** (Enter/Chip).
    *   **Click SEARCH** (Execution).
3.  **Filters**: Apply filters (Experience 5yr+) after keywords.

### Step 3: Extraction
1.  Extract **Top 10 Candidates**.
2.  Fields: Name, Title, Experience, Resume Link.

## 4. Output
*   **Path**: `talent-search/candidate/saramin/candidate_list_{Date}_saramin.csv`
