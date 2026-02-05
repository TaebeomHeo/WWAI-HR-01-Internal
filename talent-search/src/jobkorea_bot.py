from playwright.sync_api import sync_playwright
import time
import csv
import os
from datetime import datetime

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

# OpenAI Client 설정
# 주의: API Key는 코드에 직접 포함하는 것보다 환경변수로 관리하는 것이 안전합니다.
# GitHub Secret Scanning 방지를 위해 Hardcoded Key 제거
if not os.environ.get("OPENAI_API_KEY"):
    # 로컬 테스트용 (커밋하지 말 것) 또는 .env 파일 사용 권장
    pass 

client = OpenAI() # 환경변수 OPENAI_API_KEY 자동 참조

# Config 로드
CONFIG_PATH = os.path.join("talent-search", "config", "filtering_criteria.yaml")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

SEARCH_KEYWORD_EXACT = config.get("search_keywords", {}).get("exact_match", "SQA")
SEARCH_KEYWORD_MAIN = config.get("search_keywords", {}).get("integrated", "AI활용")
FILTERING_CRITERIA = config.get("criteria", [])
LLM_MODEL = config.get("llm", {}).get("model", "gpt-4o")

# 결과 파일 설정
DATE_STR = datetime.now().strftime("%Y-%m-%d")
OUTPUT_DIR = os.path.join("talent-search", "candidate", "jobkorea")
os.makedirs(OUTPUT_DIR, exist_ok=True)
CSV_FILENAME = f"candidate_list_filtered_{DATE_STR}_jobkorea.csv"
CSV_PATH = os.path.join(OUTPUT_DIR, CSV_FILENAME)

def check_candidate_with_llm(resume_text, criteria):
    """
    LLM을 사용하여 후보자 이력서(resume_text)가 기준(criteria)에 부합하는지 평가합니다.
    """
    print("  [AI 평가] OpenAI GPT-4o 분석 중...")
    
    # 텍스트 전처리 (토큰 제한 고려하여 앞부분 5000자 사용)
    short_text = resume_text[:5000]
    
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

def run():
    print("JobKorea Bot (Smart Filtering) 시작...")
    print(f"검색어: {SEARCH_KEYWORD_EXACT} (일치), {SEARCH_KEYWORD_MAIN} (통합)")
    
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
            
            # 3. 검색 조건 입력 (Config 사용)
            print("검색 조건 설정 중...")
            
            try:
                dropdown = page.locator(".search-select-type, .searchBar .select").first
                if dropdown.is_visible():
                    dropdown.click()
                    time.sleep(0.5)
                    page.locator("li:has-text('일치검색')").click()
                
                time.sleep(1)
                
                keyword_input = page.locator("#txtKeyword")
                keyword_input.click()
                page.evaluate(f"document.getElementById('txtKeyword').value = '{SEARCH_KEYWORD_EXACT}'")
                keyword_input.press("Enter")
                time.sleep(1)
                
            except Exception as e:
                print(f"일치검색 설정 실패: {e}")
            
            try:
                page.evaluate(f"document.getElementById('txtKeyword').value = '{SEARCH_KEYWORD_MAIN}'")
                keyword_input.press("Enter")
                time.sleep(1)
            except Exception as e:
                print(f"메인 키워드 입력 실패: {e}")
                
            print("검색 시작...")
            page.evaluate("document.getElementById('btnKeywordSearch').click()")
            time.sleep(5)
            
            # 4. 데이터 추출 및 필터링 (Fetch 30 & Filter)
            print("데이터 추출 및 상세 분석 중 (최대 30명)...")
            
            # 먼저 리스트에서 기본 정보 추출 (30명까지 스크롤 필요할 수 있음)
            # 간단히 스크롤 몇 번 내리기
            for _ in range(3):
                page.mouse.wheel(0, 1000)
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
                    
                    return Array.from(grouped.values()).filter(c => c.Name).slice(0, 30);
                }
            """)
            
            print(f"1차 추출 후보자 수: {len(raw_candidates)}명")
            
            final_candidates = []
            
            for cand in raw_candidates:
                print(f"[{cand['Name']}] 상세 이력서 분석 중... ({cand['Link']})")
                try:
                    # 상세 페이지 이동
                    page.goto(cand['Link'])
                    page.wait_for_load_state('domcontentloaded')
                    time.sleep(2) # 로딩 대기
                    
                    # 텍스트 추출 (전체 텍스트)
                    # body 텍스트나 특정 컨테이너 사용
                    resume_text = page.inner_text("body")
                    
                    # AI 평가 (Stub)
                    passed, reason = check_candidate_with_llm(resume_text, FILTERING_CRITERIA)
                    
                    if passed:
                        print(f"  -> 통과! ({reason})")
                        cand['Reason'] = reason
                        final_candidates.append(cand)
                    else:
                        print(f"  -> 탈락 ({reason})")
                        
                except Exception as e:
                    print(f"  -> 분석 실패: {e}")
                    # 실패해도 다음 사람 진행
                
                # 다시 리스트로 돌아갈 필요 없이 URL로 바로 이동했으므로, 
                # 다음 loop에서 바로 goto 하므로 백버튼 불필요.
            
            print(f"\n최종 선발된 후보자: {len(final_candidates)}명")
            
            # 5. CSV 저장
            if final_candidates:
                with open(CSV_PATH, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.DictWriter(f, fieldnames=['Name', 'Title', 'Experience', 'Link', 'Reason'])
                    writer.writeheader()
                    writer.writerows(final_candidates)
                print(f"\nCSV 저장 완료: {CSV_PATH}")
            else:
                print("\n조건을 만족하는 후보자가 없습니다.")

        except Exception as e:
            print(f"오류 발생: {e}")
            import traceback
            traceback.print_exc()
        finally:
            print("작업 완료. 브라우저 대기 중...")
            # context.close()


if __name__ == "__main__":
    run()
