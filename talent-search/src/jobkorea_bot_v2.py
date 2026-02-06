from playwright.sync_api import sync_playwright
import time
import csv
import os
from datetime import datetime
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

# ==================================================================================
# 설정 (Environment Setup)
# ==================================================================================
import yaml
from openai import OpenAI

# ==================================================================================
# 설정 (Environment Setup)
# ==================================================================================
USER_ID = "wisewires9"
USER_PW = "insa5051"

# Config 로드
CONFIG_PATH = os.path.join("talent-search", "config", "filtering_criteria.yaml")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# 리스트 형태로 키워드 로드 (단일 문자열도 리스트로 변환)
_exact = config.get("search_keywords", {}).get("exact_match", ["SQA"])
_integrated = config.get("search_keywords", {}).get("integrated", ["AI활용"])
SEARCH_KEYWORDS_EXACT = _exact if isinstance(_exact, list) else [_exact]
SEARCH_KEYWORDS_INTEGRATED = _integrated if isinstance(_integrated, list) else [_integrated]
FILTERING_CRITERIA = config.get("criteria", [])
LLM_MODEL = config.get("llm", {}).get("model", "gpt-4o")
OPENAI_API_KEY = config.get("llm", {}).get("api_key", "")

# OpenAI Client 설정 (Config에서 API Key 로드)
client = OpenAI(api_key=OPENAI_API_KEY)

# 결과 파일 설정
DATE_STR = datetime.now().strftime("%Y-%m-%d")
OUTPUT_DIR = os.path.join("talent-search", "candidate", "jobkorea")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 파일명에 검색 조건 포함 (일치_통합 형태)
exact_str = "_".join(SEARCH_KEYWORDS_EXACT)
integrated_str = "_".join(SEARCH_KEYWORDS_INTEGRATED)
CSV_FILENAME = f"candidate_{DATE_STR}_exact({exact_str})_integ({integrated_str}).csv"
CSV_PATH = os.path.join(OUTPUT_DIR, CSV_FILENAME)

def check_candidate_with_llm(resume_text, criteria):
    """
    LLM을 사용하여 후보자 이력서(resume_text)가 기준(criteria)에 부합하는지 평가합니다.
    """
    print("  [AI 평가] OpenAI GPT-4o 분석 중...")

    # 텍스트 전처리 (토큰 제한 고려)
    # 앞부분 3500자 + 뒷부분 1500자 (희망근무조건 등 중요 정보 보존)
    if len(resume_text) > 5000:
        short_text = resume_text[:3500] + "\n\n...[중략]...\n\n" + resume_text[-1500:]
    else:
        short_text = resume_text

    criteria_str = "\n".join([f"- {c}" for c in criteria])

    prompt = f"""
    You are an expert HR Recruiter. Evaluate if the candidate's resume matches the following Job Requirements.

    [Job Requirements]
    {criteria_str}

    [Candidate Resume]
    {short_text}

    [Task]
    Analyze the resume and determine if the candidate passes the requirements.
    Output JSON format only:
    {{
        "pass": true/false,
        "reason": "Summarize the reason in Korean (max 1 sentence). Mention matched skills."
    }}
    """

    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful HR assistant. Output JSON only."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )

        import json
        result = json.loads(response.choices[0].message.content)
        return result.get("pass", False), result.get("reason", "No reason provided")

    except Exception as e:
        print(f"  [AI Error] {e}")
        return False, f"Error: {e}"


def select_search_type_and_input(page, search_type, keyword):
    """
    검색 유형을 선택하고 키워드를 입력하는 함수

    Args:
        page: Playwright page 객체
        search_type: "exact" (일치검색) 또는 "integrated" (통합검색)
        keyword: 검색할 키워드
    """
    # data-stype 값 매핑
    # 1 = 통합검색, 9 = 일치검색
    stype = "9" if search_type == "exact" else "1"
    type_name = "일치검색" if search_type == "exact" else "통합검색"

    print(f"  [{type_name}] '{keyword}' 입력 중...")

    # 1. 검색 유형 선택 (드롭다운 옵션 직접 클릭)
    page.evaluate(f"""
        (() => {{
            const option = document.querySelector('#dvSelectSearchOption li[data-stype="{stype}"]');
            if (option) {{
                option.click();
                // 드롭다운 닫기
                const optionList = document.querySelector('#dvSelectSearchOption');
                if (optionList) optionList.style.display = 'none';
            }}
        }})()
    """)
    time.sleep(0.5)

    # 2. 키워드 입력 (argument로 전달하여 특수문자 안전 처리)
    page.evaluate("""
        (kw) => {
            const input = document.querySelector('#txtKeyword');
            if (input) {
                input.value = kw;
                input.dispatchEvent(new Event('input', {bubbles: true}));
            }
        }
    """, keyword)
    time.sleep(0.3)

    # 3. 검색 버튼 클릭
    page.evaluate("""
        (() => {
            const btn = document.querySelector('#btnKeywordSearch');
            if (btn) btn.click();
        })()
    """)
    time.sleep(1)


def run():
    print("JobKorea Bot v2 (Smart Filtering) 시작...")
    print(f"검색어: {SEARCH_KEYWORDS_EXACT} (일치), {SEARCH_KEYWORDS_INTEGRATED} (통합)")

    with sync_playwright() as p:
        # 사용자 데이터 디렉토리 설정 (세션 유지)
        user_data_dir = os.path.join(os.getcwd(), "playwright_user_data_jobkorea")

        # 브라우저 실행
        context = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            viewport={'width': 1280, 'height': 1024},
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = context.pages[0]

        try:
            # 1. 로그인 (Login)
            print("로그인 단계 진입...")
            page.goto("https://www.jobkorea.co.kr/Login/Login_Tot.asp")

            # 기업회원 탭 클릭
            corp_tab = page.locator("li[role='tab'] a:has-text('기업회원')")
            if corp_tab.is_visible():
                corp_tab.click()
                time.sleep(1)

            # 로그인 확인 및 수행
            if page.locator("input#M_ID").is_visible():
                print("로그인 시도 중...")
                page.fill("input#M_ID", USER_ID)
                page.fill("input#M_PWD", USER_PW)
                page.click("button.login-button")
                time.sleep(3)

                try:
                    if page.is_visible(".popup_layer"):
                        page.keyboard.press("Escape")
                except:
                    pass

            # 2. 인재 검색 (Talent Search)
            target_url = "https://www.jobkorea.co.kr/Corp/Person/Find"
            print(f"인재검색 페이지 이동: {target_url}")
            page.goto(target_url)
            page.wait_for_load_state('domcontentloaded')
            time.sleep(2)

            # ================================================================
            # 3. 검색 조건 입력 (v2: 수정된 로직)
            # ================================================================
            print("검색 조건 설정 중...")

            # 3-0. 기존 검색 조건 초기화
            print("  [초기화] 기존 검색 조건 초기화 시도...")
            reset_clicked = page.evaluate("""
                (() => {
                    const resetBtn = document.querySelector('#dvbtnReset');
                    if (resetBtn) {
                        resetBtn.click();
                        return true;
                    }
                    return false;
                })()
            """)
            if reset_clicked:
                print("  [초기화] 완료")
            else:
                print("  [초기화] 버튼 없음 - 스킵")
            time.sleep(1)

            # 3-1. 일치검색 키워드들 입력
            for keyword in SEARCH_KEYWORDS_EXACT:
                select_search_type_and_input(page, "exact", keyword)
                time.sleep(1)

            # 3-2. 통합검색 키워드들 입력
            for keyword in SEARCH_KEYWORDS_INTEGRATED:
                select_search_type_and_input(page, "integrated", keyword)
                time.sleep(1)

            # 검색 조건 확인 (디버깅용)
            conditions = page.evaluate("""
                (() => {
                    const buttons = document.querySelectorAll('#ulConditions button');
                    return Array.from(buttons).map(btn => btn.innerText.trim());
                })()
            """)
            print(f"적용된 검색 조건: {conditions}")

            # 최종 검색 결과 대기
            time.sleep(3)

            # 4. 데이터 추출 및 필터링 (Fetch 30 & Filter)
            print("데이터 추출 및 상세 분석 중 (최대 50명)...")

            # 50명 로드를 위해 스크롤 5회
            for _ in range(5):
                page.mouse.wheel(0, 1500)
                time.sleep(1)

            raw_candidates = page.evaluate("""
                () => {
                    const links = Array.from(document.querySelectorAll('a.dvResumeLink'));
                    const grouped = new Map();
                    const baseUrl = 'https://www.jobkorea.co.kr';

                    links.forEach(link => {
                        const href = link.getAttribute('href');
                        if (!href) return;
                        const rNoMatch = href.match(/rNo=(\\d+)/);
                        if (!rNoMatch) return;
                        const rNo = rNoMatch[1];

                        if (!grouped.has(rNo)) {
                            grouped.set(rNo, { Name: '', Title: '', Link: baseUrl + href, Experience: '' });
                        }

                        const entry = grouped.get(rNo);
                        const text = link.innerText.trim();

                        if (!entry.Name) entry.Name = text;
                        else if (text && text !== entry.Name && !entry.Title) entry.Title = text;

                        let container = link;
                        for(let i=0; i<6; i++) {
                            if (container.innerText.includes('경력')) break;
                            container = container.parentElement || container;
                        }

                        if (container.innerText.includes('경력')) {
                           const textAround = container.innerText;
                           const expMatch = textAround.match(/경력\\s*([\\d년\\s]+[\\d개월]*)/);
                           if (expMatch && !entry.Experience) {
                             entry.Experience = expMatch[0].replace('경력', '').replace(/\\s+/g, ' ').trim();
                           }
                        }
                    });

                    return Array.from(grouped.values()).filter(c => c.Name).slice(0, 50);
                }
            """)

            print(f"1차 추출 후보자 수: {len(raw_candidates)}명")

            all_candidates = []

            for idx, cand in enumerate(raw_candidates):
                print(f"[{idx+1}/{len(raw_candidates)}] [{cand['Name']}] 상세 이력서 분석 중...")
                try:
                    # 상세 페이지 이동
                    page.goto(cand['Link'])
                    page.wait_for_load_state('domcontentloaded')
                    time.sleep(2) # 로딩 대기

                    # 텍스트 추출 (전체 텍스트)
                    resume_text = page.inner_text("body")

                    # AI 평가
                    passed, reason = check_candidate_with_llm(resume_text, FILTERING_CRITERIA)

                    cand['Result'] = 'PASS' if passed else 'FAIL'
                    cand['Reason'] = reason
                    all_candidates.append(cand)

                    if passed:
                        print(f"  -> PASS ({reason})")
                    else:
                        print(f"  -> FAIL ({reason})")

                except Exception as e:
                    print(f"  -> 분석 실패: {e}")
                    cand['Result'] = 'ERROR'
                    cand['Reason'] = str(e)
                    all_candidates.append(cand)

            # PASS를 앞에, FAIL을 뒤에 정렬
            passed_candidates = [c for c in all_candidates if c.get('Result') == 'PASS']
            failed_candidates = [c for c in all_candidates if c.get('Result') != 'PASS']
            sorted_candidates = passed_candidates + failed_candidates

            print(f"\n결과: PASS {len(passed_candidates)}명 / FAIL {len(failed_candidates)}명")

            # 5. CSV 및 Excel 저장
            if sorted_candidates:
                # CSV 저장
                with open(CSV_PATH, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.DictWriter(f, fieldnames=['Result', 'Name', 'Title', 'Experience', 'Link', 'Reason'])
                    writer.writeheader()
                    writer.writerows(sorted_candidates)
                print(f"\nCSV 저장 완료: {CSV_PATH}")

                # Excel 저장
                EXCEL_PATH = CSV_PATH.replace('.csv', '.xlsx')
                wb = Workbook()
                ws = wb.active
                ws.title = "후보자 목록"

                # 헤더
                headers = ['Result', 'Name', 'Title', 'Experience', 'Link', 'Reason']
                ws.append(headers)

                # 데이터
                for cand in sorted_candidates:
                    ws.append([cand.get(h, '') for h in headers])

                # 컬럼 너비 설정
                col_widths = {
                    'A': 8,   # Result
                    'B': 10,  # Name
                    'C': 35,  # Title
                    'D': 12,  # Experience
                    'E': 60,  # Link
                    'F': 80,  # Reason
                }
                for col, width in col_widths.items():
                    ws.column_dimensions[col].width = width

                wb.save(EXCEL_PATH)
                print(f"Excel 저장 완료: {EXCEL_PATH}")
            else:
                print("\n후보자가 없습니다.")

        except Exception as e:
            print(f"오류 발생: {e}")
            import traceback
            traceback.print_exc()
        finally:
            print("작업 완료. 브라우저 유지 중...")
            print("브라우저를 종료하려면 Enter를 누르세요.")
            input()
            # context.close()


if __name__ == "__main__":
    run()
