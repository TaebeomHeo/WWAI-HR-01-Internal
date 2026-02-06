import os
import time
import csv
import re
import yaml
import json
from datetime import datetime
from playwright.sync_api import sync_playwright
from openpyxl import Workbook
from openai import OpenAI

# ==================================================================================
# 설정 (Environment Setup)
# ==================================================================================
LOGIN_URL = 'https://www.saramin.co.kr/zf_user/auth'
SEARCH_URL = 'https://www.saramin.co.kr/zf_user/memcom/talent-pool/main/search'
USER_ID = 'wisewires'
USER_PW = 'insa5051'

# Config 로드
CONFIG_PATH = os.path.join("talent-search", "config", "filtering_criteria.yaml")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# 리스트 형태로 키워드 로드 (단일 문자열도 리스트로 변환)
_exact = config.get("search_keywords", {}).get("exact_match", ["개발"])
_integrated = config.get("search_keywords", {}).get("integrated", ["금융"])
SEARCH_KEYWORDS_EXACT = _exact if isinstance(_exact, list) else [_exact]
SEARCH_KEYWORDS_INTEGRATED = _integrated if isinstance(_integrated, list) else [_integrated]
FILTERING_CRITERIA = config.get("criteria", [])
LLM_MODEL = config.get("llm", {}).get("model", "gpt-4o")
OPENAI_API_KEY = config.get("llm", {}).get("api_key", "")

# OpenAI Client 설정
client = OpenAI(api_key=OPENAI_API_KEY)

# 결과 파일 설정
DATE_STR = datetime.now().strftime("%Y-%m-%d")
OUTPUT_DIR = os.path.join("talent-search", "candidate", "saramin")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 파일명에 검색 조건 포함
exact_str = "_".join(SEARCH_KEYWORDS_EXACT)
integrated_str = "_".join(SEARCH_KEYWORDS_INTEGRATED)
CSV_FILENAME = f"candidate_{DATE_STR}_or({exact_str})_and({integrated_str}).csv"
CSV_PATH = os.path.join(OUTPUT_DIR, CSV_FILENAME)


def check_candidate_with_llm(resume_text, criteria):
    """
    LLM을 사용하여 후보자 이력서(resume_text)가 기준(criteria)에 부합하는지 평가합니다.
    """
    print("  [AI 평가] OpenAI GPT 분석 중...")

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

        result = json.loads(response.choices[0].message.content)
        return result.get("pass", False), result.get("reason", "No reason provided")

    except Exception as e:
        print(f"  [AI Error] {e}")
        return False, f"Error: {e}"


def run():
    print("Saramin Bot v2 (Smart Filtering) 시작...")
    print(f"검색어: {SEARCH_KEYWORDS_EXACT} (OR/일치), {SEARCH_KEYWORDS_INTEGRATED} (AND/통합)")
    print(f"필터링 기준: {FILTERING_CRITERIA}")

    # 사용자 데이터 디렉토리 설정 (로그인 세션 유지용)
    user_data_dir = os.path.join(os.getcwd(), 'playwright_user_data')
    os.makedirs(user_data_dir, exist_ok=True)

    with sync_playwright() as p:
        # 1. 브라우저 실행 (Persistent Context 사용)
        print(f"사용자 데이터 디렉토리: {user_data_dir}")
        context = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            viewport={'width': 1280, 'height': 1024}
        )
        page = context.pages[0] if context.pages else context.new_page()

        try:
            # 2. 로그인 페이지 이동
            print(f"로그인 페이지로 이동 중: {LOGIN_URL}")
            page.goto(LOGIN_URL, timeout=60000)

            # 이미 로그인 되어 있는지 확인 (Persistent Context 효과)
            if "login" not in page.url and "auth" not in page.url:
                 print("이미 로그인되어 있을 수 있습니다.")
            else:
                # 3. 기업회원 탭 클릭 (로그인 페이지인 경우에만)
                if page.is_visible('.btn_tab.t_com'):
                    print("기업회원 탭 클릭...")
                    page.click('.btn_tab.t_com')

                # 4. 로그인 정보 입력 (로그인 페이지인 경우에만)
                if page.is_visible("#id"):
                    print("아이디/비밀번호 입력 중...")
                    page.fill("#id", USER_ID)
                    page.fill("#password", USER_PW)

                    # 5. 로그인 버튼 클릭
                    print("로그인 버튼 클릭...")
                    page.click('.btn_login')

                    # 페이지 이동 대기
                    page.wait_for_load_state('networkidle')

            # 6. 인재풀 검색 페이지 이동
            print(f"인재풀 검색 페이지로 이동 중: {SEARCH_URL}")
            page.goto(SEARCH_URL)

            print("페이지 로딩 대기 중... (2차 인증이 필요한 경우 브라우저에서 직접 완료해주세요.)")
            page.wait_for_selector('.talent_header', timeout=0)

            # 7. 검색 조건 초기화
            if page.is_visible('button.btn_reset'):
                print("검색 조건 초기화...")
                page.click('button.btn_reset')
                time.sleep(1)

            # 검색 패널 열기 (필요시)
            if not page.is_visible('div.search_default'):
                page.click('#app > div.talent_header > div > div > div.btn_search_history_wrap > button')

            # ================================================================
            # 8. OR 키워드 입력 (exact_match → OR 검색, 정확히 일치)
            # ================================================================
            for keyword in SEARCH_KEYWORDS_EXACT:
                print(f"OR 키워드 '{keyword}' 입력 중 (정확히 일치)...")
                page.click('div.search_default input.search_input.result')
                page.wait_for_selector('.search_detail input.search_input')

                page.evaluate(f"""
                    () => {{
                        const input = document.querySelector(".search_detail input.search_input");
                        input.value = "{keyword}";
                        input.dispatchEvent(new Event("input", {{bubbles:true}}));

                        const exactMatch = document.querySelector("#keywordSearch");
                        if (exactMatch) {{
                            exactMatch.checked = true; // Exact Match ON
                            exactMatch.dispatchEvent(new Event("change", {{bubbles: true}}));
                        }}
                    }}
                """)

                page.click('.search_detail input.search_input')
                page.press('.search_detail input.search_input', 'Enter')
                time.sleep(1)

            # ================================================================
            # 9. AND 키워드 입력 (integrated → AND 검색, 포함)
            # ================================================================
            for keyword in SEARCH_KEYWORDS_INTEGRATED:
                print(f"AND 키워드 '{keyword}' 입력 중 (포함)...")
                page.click('div.search_word_include input.search_input.result')
                page.wait_for_selector('.search_detail input.search_input')

                page.evaluate(f"""
                    () => {{
                        const input = document.querySelector(".search_detail input.search_input");
                        if (input) {{
                            input.value = "{keyword}";
                            input.dispatchEvent(new Event("input", {{bubbles:true}}));

                            const exactMatch = document.querySelector("#keywordSearch");
                            if (exactMatch) {{
                                exactMatch.checked = false; // Exact Match OFF
                                exactMatch.dispatchEvent(new Event("change", {{bubbles: true}}));
                            }}
                        }}
                    }}
                """)

                page.click('.search_detail input.search_input')
                page.press('.search_detail input.search_input', 'Enter')
                time.sleep(1)

            # 10. 검색 결과 대기
            print("검색 결과 업데이트 대기 중...")
            time.sleep(5)
            page.wait_for_selector('.talent_list_item', timeout=10000)
            time.sleep(2)

            # 11. 결과 추출 (기본 정보)
            print("결과 추출 중...")

            basic_candidates = page.evaluate("""
                () => {
                    const listItems = Array.from(document.querySelectorAll('.talent_list_item'));

                    return listItems.slice(0, 30).map(item => {
                        const personInfo = item.querySelector('.personal_info');
                        const name = personInfo?.querySelector('.name')?.innerText.trim() || "";
                        const genderAge = personInfo?.querySelector('.gender_age')?.innerText.trim() || "";
                        const careerAll = personInfo?.querySelector('.career_all')?.innerText.trim() || "";
                        const residx = item.querySelector('.check_area')?.getAttribute('residx') || "";

                        return {
                            name: name,
                            gender_age: genderAge,
                            career_all: careerAll,
                            residx: residx
                        };
                    });
                }
            """)

            print(f"1차 추출 완료 (총 {len(basic_candidates)}명). 상세 분석 시작...")

            all_candidates = []

            # ================================================================
            # 12. 상세 정보 추출 + AI 필터링
            # ================================================================
            for idx, cand in enumerate(basic_candidates):
                if not cand['residx']:
                    continue

                detail_url = f"https://hiring.saramin.co.kr/applicant-view/position/resume/{cand['residx']}"
                api_url = f"https://api-hiring.saramin.co.kr/api/positions/resume/{cand['residx']}/files?"
                print(f"[{idx+1}/{len(basic_candidates)}] [{cand['name']}] API 호출 중...")

                try:
                    # API를 통해 이력서 HTML 가져오기
                    resume_data = page.evaluate(f"""
                        async () => {{
                            try {{
                                const response = await fetch('{api_url}', {{
                                    credentials: 'include'
                                }});
                                const data = await response.json();

                                if (data.success && data.result && data.result.resumeHtml) {{
                                    const parser = new DOMParser();
                                    const doc = parser.parseFromString(data.result.resumeHtml, 'text/html');
                                    return {{
                                        success: true,
                                        text: doc.body.innerText,
                                        htmlLength: data.result.resumeHtml.length
                                    }};
                                }}
                                return {{ success: false, error: 'No resumeHtml in response' }};
                            }} catch(e) {{
                                return {{ success: false, error: e.message }};
                            }}
                        }}
                    """)

                    address = ""
                    resume_text = ""

                    if resume_data.get('success'):
                        resume_text = resume_data.get('text', '')
                        print(f"  이력서 텍스트: {len(resume_text)}자")

                        # 주소 추출
                        addr_match = re.search(r'(서울|경기|인천|부산|대구|광주|대전|울산|세종|강원|충북|충남|전북|전남|경북|경남|제주)\s*[가-힣]+(구|시|군)', resume_text)
                        if addr_match:
                            address = addr_match.group(0).strip()

                        # AI 필터링
                        if FILTERING_CRITERIA:
                            passed, reason = check_candidate_with_llm(resume_text, FILTERING_CRITERIA)
                            cand['Result'] = 'PASS' if passed else 'FAIL'
                            cand['Reason'] = reason
                            if passed:
                                print(f"  -> PASS ({reason})")
                            else:
                                print(f"  -> FAIL ({reason})")
                        else:
                            cand['Result'] = 'N/A'
                            cand['Reason'] = 'No filtering criteria'
                            print(f"  -> 필터링 기준 없음")

                    else:
                        print(f"  API 오류: {resume_data.get('error', 'Unknown')}")
                        cand['Result'] = 'ERROR'
                        cand['Reason'] = resume_data.get('error', 'API Error')

                    cand['Address'] = address
                    cand['Link'] = detail_url
                    all_candidates.append(cand)

                    time.sleep(0.5)

                except Exception as e:
                    print(f"  오류: {e}")
                    cand['Address'] = ""
                    cand['Link'] = detail_url
                    cand['Result'] = 'ERROR'
                    cand['Reason'] = str(e)
                    all_candidates.append(cand)

            # ================================================================
            # 13. 결과 정렬 (PASS를 앞에)
            # ================================================================
            passed_candidates = [c for c in all_candidates if c.get('Result') == 'PASS']
            failed_candidates = [c for c in all_candidates if c.get('Result') != 'PASS']
            sorted_candidates = passed_candidates + failed_candidates

            print(f"\n결과: PASS {len(passed_candidates)}명 / FAIL {len(failed_candidates)}명")

            # ================================================================
            # 14. CSV 및 Excel 저장
            # ================================================================
            if sorted_candidates:
                # CSV 저장
                headers = ['Result', 'Name', 'Gender_Age', 'Career', 'Address', 'Link', 'Reason']
                with open(CSV_PATH, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f)
                    writer.writerow(headers)
                    for c in sorted_candidates:
                        writer.writerow([
                            c.get('Result', ''),
                            c.get('name', ''),
                            c.get('gender_age', ''),
                            c.get('career_all', ''),
                            c.get('Address', ''),
                            c.get('Link', ''),
                            c.get('Reason', '')
                        ])
                print(f"\nCSV 저장 완료: {CSV_PATH}")

                # Excel 저장
                EXCEL_PATH = CSV_PATH.replace('.csv', '.xlsx')
                wb = Workbook()
                ws = wb.active
                ws.title = "후보자 목록"

                ws.append(headers)
                for c in sorted_candidates:
                    ws.append([
                        c.get('Result', ''),
                        c.get('name', ''),
                        c.get('gender_age', ''),
                        c.get('career_all', ''),
                        c.get('Address', ''),
                        c.get('Link', ''),
                        c.get('Reason', '')
                    ])

                # 컬럼 너비 설정
                col_widths = {'A': 8, 'B': 10, 'C': 12, 'D': 15, 'E': 15, 'F': 60, 'G': 80}
                for col, width in col_widths.items():
                    ws.column_dimensions[col].width = width

                wb.save(EXCEL_PATH)
                print(f"Excel 저장 완료: {EXCEL_PATH}")
            else:
                print("\n후보자가 없습니다.")

            print("\n완료!")

        except Exception as e:
            print(f"오류 발생: {e}")
            import traceback
            traceback.print_exc()

        finally:
            print("작업 완료. 브라우저는 열린 상태로 유지됩니다.")
            print("브라우저를 종료하려면 Enter를 누르세요...")
            try:
                input()
            except EOFError:
                pass

if __name__ == "__main__":
    run()
