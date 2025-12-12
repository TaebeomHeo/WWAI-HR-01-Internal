# JobKorea Search Automation Implementation Details

## 1. Objective
Automate the extraction of direct applicants for a specific JobKorea job posting, filtering out generic/AI-recommended candidates.

## 2. Target URL
- URL: `https://www.jobkorea.co.kr/Corp/Applicant/list?GI_No=50027324`
- **Authentication**: Requires Login.

## 3. Filtering Logic (Direct vs Related)
- **Direct Applicants**: Full names are visible (e.g., "홍길동").
- **Related/AI Applicants**: Names are masked (e.g., "홍○○") or marked as AI recommendations.
- **Rule**: Exclude any name containing "○○" or "*".

## 4. Pagination
- **Selector**: `div.tplPagination.newVer`
- **Logic**:
  - Iterate through page numbers explicitly (e.g., `a[data-page="2"]`).
  - **Important**: The page does *not* fully refresh the DOM in a standard way that Selenium/Puppeteer might expect as a "new page load" event. It uses AJAX.
  - **Wait Condition**: Wait for the list container to update or a fixed delay after clicking.

## 5. Data Extraction
- **Container**: `a.applicant-box.devTypeAplctHref`
- **Fields**:
  - **Name**: `div > div:nth-of-type(1)` inside the container.
  - **Metadata** (Age, Gender, etc.): `ul.list-txt li`.
    - Format: "남 만 26세", "대졸(4년)", "경력 2년" etc.
    - Strategy: Extract full text and parse with Regex.

## 6. Migration to Node.js
- **Library**: Puppeteer (for browser automation) + xlsx (for Excel saving).
- **Structure**:
  - `crawler.js`: Main script.
  - `package.json`: Dependencies.
