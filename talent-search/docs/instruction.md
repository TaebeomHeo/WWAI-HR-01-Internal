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
1.  Navigate to **Talent Search (인재검색)**: `https://www.jobkorea.co.kr/Corp/Talent/Search/List`
2.  Locate the search input field (placeholder containing "키워드").
3.  Enter the **Target Keyword**.
4.  Click the **Search Button** (magnifying glass icon).
5.  Wait for results to load.

### Step 3: Extraction & Output
1.  Identify the list of candidates.
2.  Extract the following fields for the **Top 5 Candidates**:
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
