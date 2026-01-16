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

### Step 2: Talent Search Protocol
**User Input Format**:
*   `일치 검색 : [Keyword]` -> Action: Enter in Left Search Bar + Toggle **"Exact Match" ON**.
*   `검색 : [Keyword]` -> Action: Enter in **"AND"** Search Bar.
*   **Logic**: All inputs (single or multiple) must be combined as **AND** conditions.

**Current Execution**:
1.  **Exact Match**: "QA" (Entered)
2.  **AND Search**: "개발" (Entered)
3.  **Execute**: Click **Search** button.

### Step 3: Extraction
1.  Extract **Top 10 Candidates**.
2.  Fields: Name, Title, Experience, Resume Link.

## 4. Output
*   **Path**: `talent-search/candidate/saramin/candidate_list_{Date}_saramin.csv`
