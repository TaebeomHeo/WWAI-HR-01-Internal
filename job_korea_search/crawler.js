const puppeteer = require('puppeteer');
const xlsx = require('xlsx');
require('dotenv').config({ path: '../.env' }); // Adjust path if .env is in root

(async () => {
    // Configuration
    const TARGET_URL = 'https://www.jobkorea.co.kr/Corp/Applicant/list?GI_No=50027324';
    const USER_ID = process.env.JOBKOREA_ID || 'wisewires9';
    const USER_PW = process.env.JOBKOREA_PW || 'insa5051';

    console.log("Launching browser...");
    const browser = await puppeteer.launch({
        headless: false, // Seen by user
        defaultViewport: null,
        args: ['--start-maximized']
    });

    const page = await browser.newPage();

    try {
        console.log(`Navigating to ${TARGET_URL}...`);
        await page.goto(TARGET_URL, { waitUntil: 'networkidle2' });

        // Login Check
        if (page.url().includes('Login') || page.url().includes('login')) {
            console.log("Login required. Attempting auto-login...");

            // Selectors need to be verified, using generic fallback logic or known IDs
            // JobKorea corporate login often uses #M_ID, #M_PWD
            try {
                await page.waitForSelector('input[name="M_ID"], #lb_id', { timeout: 5000 });
                await page.type('input[name="M_ID"], #lb_id', USER_ID);
                await page.type('input[name="M_PWD"], #lb_pw', USER_PW);
                await page.keyboard.press('Enter');

                await page.waitForNavigation({ waitUntil: 'networkidle2' });
                console.log("Login submitted.");

                // Return to target if redirected to main
                if (!page.url().includes('Applicant/list')) {
                    await page.goto(TARGET_URL, { waitUntil: 'networkidle2' });
                }
            } catch (e) {
                console.log("Auto-login failed or selectors changed. Please login manually.");
                await page.waitForFunction(() => !window.location.href.includes('Login'), { timeout: 60000 });
            }
        }

        console.log("Processing Applicant List...");

        let allApplicants = [];
        let hasNextPage = true;
        let currentPage = 1;

        while (hasNextPage) {
            console.log(`Scraping Page ${currentPage}...`);
            await new Promise(r => setTimeout(r, 3000)); // Wait for render

            // Extract Data
            const applicants = await page.evaluate(() => {
                const results = [];
                const boxes = document.querySelectorAll('a.applicant-box.devTypeAplctHref');

                boxes.forEach(box => {
                    const nameDiv = box.querySelector('div > div:nth-of-type(1)');
                    const name = nameDiv ? nameDiv.innerText.trim() : '';

                    // Filter Logic: Exclude '○○' or empty
                    if (name && !name.includes('○○') && !name.includes('*') && name.length > 1) {

                        // Metadata extraction
                        let metadata = '';
                        const listItems = box.querySelectorAll('ul.list-txt li');
                        listItems.forEach(li => metadata += li.innerText.trim() + ' ');

                        results.push({ name, metadata: metadata.trim() });
                    }
                });
                return results;
            });

            // Add unique applicants
            const initialCount = allApplicants.length;
            applicants.forEach(app => {
                // Simple duplicate check by name (could be improved)
                if (!allApplicants.find(a => a.name === app.name)) {
                    allApplicants.push(app);
                }
            });
            console.log(`Found ${applicants.length} valid applicants on this page.`);

            // Pagination Logic
            const nextPageNum = currentPage + 1;
            const nextPageSelector = `div.tplPagination.newVer a[data-page="${nextPageNum}"]`;

            // Check if next page exists
            const nextLink = await page.$(nextPageSelector);
            if (nextLink) {
                console.log(`Clicking Page ${nextPageNum}...`);
                await nextLink.click();
                // Wait for "spinner" or just generic time
                await new Promise(r => setTimeout(r, 3000));
                currentPage++;
            } else {
                console.log("No more pages found.");
                hasNextPage = false;
            }

            // Safety break
            if (currentPage > 5) hasNextPage = false;
        }

        console.log(`\nTotal Valid Applicants: ${allApplicants.length}`);

        // Parse Details
        const parsedData = allApplicants.map(app => {
            const meta = app.metadata;

            // Regex parsing (same logic as Python)
            let gender = "Unknown";
            if (meta.includes('남')) gender = "남";
            if (meta.includes('여')) gender = "여";

            const ageMatch = meta.match(/만\s*(\d+)세/);
            const age = ageMatch ? ageMatch[1] : "";

            let education = "";
            const eduTerms = ["대졸", "초대졸", "고졸", "대학원", "박사", "석사"];
            for (const term of eduTerms) {
                if (meta.includes(term)) {
                    // Try to grab context
                    const eduMatch = meta.match(new RegExp(`(${term}[^\\s]*)`));
                    education = eduMatch ? eduMatch[1] : term;
                    break;
                }
            }

            let career = "신입";
            const careerMatch = meta.match(/경력\s*([^\s]+)/);
            if (careerMatch) career = "경력 " + careerMatch[1];

            return {
                "이름": app.name,
                "성별": gender,
                "나이": age,
                "학력": education,
                "경력": career,
                "원본_메타데이터": meta
            };
        });

        // Save to Excel
        const wb = xlsx.utils.book_new();
        const ws = xlsx.utils.json_to_sheet(parsedData);
        xlsx.utils.book_append_sheet(wb, ws, "Applicants");
        xlsx.writeFile(wb, "jobkorea_applicants_final.xlsx");

        console.log("Data saved to jobkorea_applicants_final.xlsx");

    } catch (error) {
        console.error("An error occurred:", error);
    } finally {
        await browser.close();
    }
})();
