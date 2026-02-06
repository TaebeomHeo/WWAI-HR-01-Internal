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

## 3. UI Selectors Reference (Configuration)

| Component            | Selector                                                                      | Note                                  |
| :------------------- | :---------------------------------------------------------------------------- | :------------------------------------ |
| **Login - Tab**      | `.btn_tab.t_com`                                                              | Corporate Member Tab                  |
| **Login - ID**       | `#id`                                                                         |                                       |
| **Login - PW**       | `#password`                                                                   |                                       |
| **Login - Submit**   | `.btn_login`                                                                  |                                       |
| **Search - Reset**   | `button.btn_reset`                                                            | **User Provided**                     |
| **Search - History** | `#app > div.talent_header > div > div > div.btn_search_history_wrap > button` | **User Provided** (Open Search Panel) |
| **Search - Execute** | `#search_btn` (Verify) or `button.btn_search`                                 | Click to Run Search                   |
| **Input - OR**       | `div.search_default`                                                          | Main Keyword                          |
| **Input - AND**      | `div.search_word_include`                                                     | 'Must Include'                        |
| **Input - NOT**      | `div.search_word_except`                                                      | 'Exclude'                             |
| **Input (Trigger)**  | `input.search_input.result`                                                   | Click to open Popup                   |
| **Input (Typing)**   | `.search_detail input.search_input`                                           | Inside Popup                          |
| **Toggle (Exact)**   | `#keywordSearch`                                                              | Check=Exact, Uncheck=Contains         |
| **List Item**        | `.talent_list_item`                                                           | Candidate Row                         |
| **Candidate Name**   | `.name`                                                                       |                                       |
| **Candidate ID**     | `.check_area [residx]`                                                        | Attribute extraction                  |

## 4. Execution Steps (SOP)

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

1.  **Initialize Search State**:
    - **Check for Reset Button**: Check if `button.btn_reset` is visible.
    - **Action**: If visible, click it.
    - **Open Search Panel**: Click `#app > div.talent_header > div > div > div.btn_search_history_wrap > button` if search inputs are not visible.

2.  **Search Field Interaction Logic**:
    - **Structure**:
      - OR Search: `div.search_default`
      - AND Search: `div.search_word_include`
      - NOT Search: `div.search_word_except`
    - **Protocol**:
      1.  **Select Type**: Locate the container (e.g., AND=`div.search_word_include`).
      2.  **Open Detail Popup**: Click the input field `input.search_input.result` within that container.
      3.  **Input Keyword**: In the opened popup (`.search_detail`), type into `input.search_input`.
      4.  **Exact Match**: Check `#keywordSearch` (Checkbox) if required.
      5.  **Confirm**: Press Enter or click request button.

3.  **Execution Sequence (Convention Example)**:
    - **Target**:
      - **OR**: "개발" (Exact Match: **ON**)
      - **AND**: "증권", "보험" (Exact Match: **OFF**)
    - **Action**:
      1.  **OR Keyword ("개발")**:
          - Locate **OR Input** (`div.search_default`).
          - Click `input.search_input.result`.
          - **Step A**: Type "개발" into the popup input.
          - **Step B**: _After typing_, locate and **Check** `#keywordSearch` (Exact Match: ON).
          - **Step C**: Press Enter.
      2.  **AND Keyword 1 ("증권")**:
          - Locate **AND Input** (`div.search_word_include`).
          - Click `input.search_input.result`.
          - **Step A**: Type "증권".
          - **Step B**: _After typing_, locate and **Uncheck** `#keywordSearch` (Exact Match: OFF).
          - **Step C**: Press Enter.
      3.  **AND Keyword 2 ("보험")**:
          - (If popup closed) Re-click **AND Input**.
          - **Step A**: Type "보험".
          - **Step B**: _After typing_, verify/Uncheck `#keywordSearch` (Exact Match: OFF).
          - **Step C**: Press Enter.
      4.  **Finalize**:
          - Close popup or Click Search.
    - **Filters**: Apply filters (Experience 5yr+) after keywords.

### Step 3: Extraction

1.  **Target Container**: `.talent_list > .talent_list_item`
2.  **Data Mappings**:
    - **Candidate ID**: Extract `residx` attribute from `.check_area` (Used to construct Revisit URL).
    - **Revisit URL**: `https://hiring.saramin.co.kr/applicant-view/position/resume/{residx}`
    - **Name**: `.name` (Text content)
    - **Job Title**: `.job_tit` (Text content)
    - **Career**: `.career` (Text content)
    - **Demographics/Info**: `.info` (Text content)
3.  **Process**:
    - Iterate through the first 10 items.
    - Extract fields.
    - Construct URL suitable for direct access (Note: Session required).
4.  **Save to CSV**:
    - Headers: `Name`, `Job_Title`, `Career`, `Info`, `Revisit_URL`

## 4. Output

- **Path**: `talent-search/candidate/saramin/candidate_list_{Date}_saramin.csv`
