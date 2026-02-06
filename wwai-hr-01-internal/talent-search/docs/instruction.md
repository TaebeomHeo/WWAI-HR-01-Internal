# JobKorea Talent Search - AI Instruction Manual

This document serves as a standard operating procedure (SOP) for the AI Agent to perform talent search on JobKorea.

## 1. Input Variables
When triggering this instruction, the user must provide:
*   **Target Keyword**: (e.g., "SQA", "Finance", "Java")
*   **Search Date**: (Today's date in YYYY-MM-DD format)

## 2. Pre-requisites
*   **Credentials**:
    *   ID: `wisewires9`
    *   PW: `insa5051`
*   **Tools**: Browser Tool (Headful/Headless), File System.

## 3. Execution Steps

### Step 1: Login (Corporate Member)
1.  Open Browser and navigate to `https://www.jobkorea.co.kr/Login/Login_Tot.asp`.
2.  Click the **"기업회원" (Corporate Member)** tab.
3.  Enter ID and PW.
4.  Click Login.
5.  **Verify**: Ensure redirection to the main dashboard or presence of "Logout" button.

### Step 2: Search
1.  Navigate to **Talent Search**: `https://www.jobkorea.co.kr/Corp/Person/Find`
2.  **Keyword Entry** (Repeat for each keyword):
    *   **Goal**: Find candidates matching "SQA" (Exact) AND "Financial/Banking" (Integrated) keywords.
    *   **Method A (Preferred - "Result Within Search")**:
        1.  First, search for **"SQA"** with **"일치검색" (Exact Match)**.
        2.  In the result page, check the **"결과 내 재검색" (Search within results)** box (usually near the search bar).
        3.  Enter **"금융"** (or target secondary keyword) and search.
        4.  **Important**: Ensure English/Standard keywords are typed, but for Korean keywords, if automation fails, use clipboard/value injection instead of direct typing.
    *   **Method B (Alternative)**: Use "상세검색" (Detailed Search) > Enter "SQA" in "Exact Match" field and "금융" in "Keywords" field.
4.  Click the **Search Button**.
5.  Wait for results to load.

### Step 3: Extraction & Output
1.  Identify the list of candidates.
2.  Extract the following fields for the **Top 10 Candidates**:
    *   **Name** (e.g., 홍길동)
    *   **Info/Title** (e.g., QA Team Lead at Company X)
    *   **Experience** (e.g., 10년 2개월)
    *   **Link** (Full URL to resume)
3.  Format the data into a CSV file.
    *   **Filename**: `candidate_list_{Date}_{Keyword}.csv`
    *   **Path**: `talent-search/candidate/`
    *   **Header**: `Name, Title, Experience, Link`

## 4. Completion
*   Notify the user with the path of the generated CSV file.
