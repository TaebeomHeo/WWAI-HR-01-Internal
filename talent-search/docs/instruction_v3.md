# JobKorea Talent Search - AI Instruction Manual (v3)

**Version 3**: Updated to address common automation failures (Korean input issues, element detection, and extraction accuracy).

## 1. Input Variables
When triggering this instruction, the user must provide:
*   **Target Keyword (Exact Match)**: (e.g., "SQA")
*   **Integrated Keyword**: (e.g., "AI활용", "Finance")
*   **Search Date**: (Today's date in YYYY-MM-DD format)

## 2. Pre-requisites
*   **Credentials**:
    *   ID: `wisewires9`
    *   PW: `insa5051`
*   **Tools**: Browser Tool (Headful/Headless), File System.
*   **Critical Rule**: Do NOT ask for confirmation on standard steps defined below. Execute autonomously.

## 3. Execution Steps

### Step 1: Login (Corporate Member)
1.  Open Browser and navigate to `https://www.jobkorea.co.kr/Login/Login_Tot.asp`.
2.  Select the **"기업회원" (Corporate Member)** tab.
3.  Enter ID and PW.
4.  Click Login.
5.  **Exception Handling**:
    *   If a "2-Step Authentication" (2단계 인증) popup appears, click **"다음에 변경하기"** (Change Later) or close the modal.
    *   Verify login by checking for "Logout" button or dashboard access.

### Step 2: Search (Robust Method)
1.  Navigate to **Talent Search**: `https://www.jobkorea.co.kr/Corp/Person/Find`
2.  **Apply Search Conditions**:
    *   **Goal**: Apply BOTH "Exact Match" and "Integrated Search" terms.
    *   **Input Strategy (IMPORTANT)**: Specifying Korean text directly using keyboard emulation (`press_key`) often fails. **ALWAYS use JavaScript injection** for text inputs.
    
    **Action Sequence**:
    1.  **Exact Match**: Locate the "일치검색" field (often a specific input or checkbox logic). If an input exists, inject the value:
        ```javascript
        // Example Selector (verify in DOM)
        document.querySelector('input[placeholder*="일치"]').value = "SQA"; 
        ```
    2.  **Integrated Search**: Locate the main keyword input (e.g., `#txtKeyword`). Inject the value:
        ```javascript
        document.querySelector('#txtKeyword').value = "AI활용";
        ```
    3.  **Submit**: Click the Search button via JS or Mouse Click.
        ```javascript
        document.querySelector('#btnKeywordSearch').click();
        ```

3.  Wait for results to load (use `wait` tool or `waitForSelector`).

### Step 3: Extraction (Group by Resume ID)
*   **Challenge**: The DOM often contains multiple links per candidate, leading to duplicates or mismatched data if scraped sequentially.
*   **Solution**: Group by `rNo` (Resume Number) found in the URL query string.

**Recommended Extraction Logic (JS)**:
```javascript
(() => {
  const links = Array.from(document.querySelectorAll('a.dvResumeLink'));
  const grouped = new Map();
  const baseUrl = 'https://www.jobkorea.co.kr';

  links.forEach(link => {
    const href = link.getAttribute('href');
    if (!href) return;
    const rNoMatch = href.match(/rNo=(\d+)/);
    if (!rNoMatch) return;
    const rNo = rNoMatch[1];
    
    if (!grouped.has(rNo)) {
      grouped.set(rNo, { Name: '', Title: '', Link: baseUrl + href, Experience: '' });
    }
    
    const entry = grouped.get(rNo);
    const text = link.innerText.trim();
    
    // Heuristic: Name is usually the first link text encountered for an rNo
    if (!entry.Name) entry.Name = text;
    else if (text && text !== entry.Name && !entry.Title) entry.Title = text;
    
    // Robust Experience Extraction: tailored for Korean format "경력 00년 00개월"
    let container = link;
    // Walk up the DOM to find the resume container
    for(let i=0; i<6; i++) {
        if (container.innerText.includes('경력')) break;
        container = container.parentElement || container;
    }
    
    if (container.innerText.includes('경력')) {
       const textAround = container.innerText;
       const expMatch = textAround.match(/경력\s*([\d년\s]+[\d개월]*)/); // Matches "경력 3년 6개월"
       if (expMatch && !entry.Experience) {
         entry.Experience = expMatch[0].replace('경력', '').replace(/\s+/g, ' ').trim();
       }
    }
  });

  return Array.from(grouped.values()).filter(c => c.Name).slice(0, 10);
})()
```

### Step 4: Output
1.  Save the data to a CSV file.
    *   **Filename**: `candidate_list_{Date}_{Keyword}.csv`
    *   **Path**: `talent-search/candidate/`
    *   **Header**: `Name, Title, Experience, Link`
2.  Notify the user with the file path.

## 4. Key Lessons & Troubleshooting
*   **Korean Input**: Never trust `browser_press_key` for Hangul. Use `execute_browser_javascript` to set `.value`.
*   **Selectors**: IDs like `#txtKeyword` are reliable. Verify them if search fails.
*   **Popups**: Always expect and handle "2FA" or "Event" popups on the login/home screen.
