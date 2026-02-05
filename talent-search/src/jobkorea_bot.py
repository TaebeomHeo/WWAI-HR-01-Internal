from playwright.sync_api import sync_playwright
import time
import csv
import os
from datetime import datetime

# ==================================================================================
# 설정 (Environment Setup)
# ==================================================================================
USER_ID = "wisewires9"
USER_PW = "insa5051"
SEARCH_KEYWORD_EXACT = "SQA"
SEARCH_KEYWORD_MAIN = "AI활용"

# 결과 파일 설정
DATE_STR = datetime.now().strftime("%Y-%m-%d")
OUTPUT_DIR = os.path.join("talent-search", "candidate", "jobkorea")
os.makedirs(OUTPUT_DIR, exist_ok=True)
CSV_FILENAME = f"candidate_list_{DATE_STR}_jobkorea.csv"
CSV_PATH = os.path.join(OUTPUT_DIR, CSV_FILENAME)

def run():
    print("JobKorea Bot 시작...")
    
    with sync_playwright() as p:
        # 사용자 데이터 디렉토리 설정 (세션 유지)
        user_data_dir = os.path.join(os.getcwd(), "playwright_user_data_jobkorea")
        
        print(f"사용자 데이터 디렉토리: {user_data_dir}")
        
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
            # '기업회원' 탭이 활성화되어 있는지 확인 후 클릭
            corp_tab = page.locator("li[role='tab'] a:has-text('기업회원')")
            if corp_tab.is_visible():
                corp_tab.click()
                time.sleep(1)
            
            # 로그인 확인 (이미 로그인 되어있는지)
            if page.locator("input#M_ID").is_visible():
                print("로그인 시도 중...")
                page.fill("input#M_ID", USER_ID)
                page.fill("input#M_PWD", USER_PW)
                
                # 로그인 버튼 클릭
                page.click("button.login-button") # verified by browser agent
                # 또는 type='submit'
                # page.locator("button[type='submit']").click()
                
                time.sleep(3)
                
                # 2단계 인증 팝업 등 예외 처리
                # (팝업이 뜬다면 '다음에 변경하기' 등을 클릭해야 함. 여기서는 수동 개입 시간을 줌)
                # Instruction: "Click '다음에 변경하기' or close modal."
                try:
                    # 팝업 닫기 시도 (예시 Selector)
                    if page.is_visible(".popup_layer"): # 일반적인 팝업 클래스 가정
                        print("팝업 감지. 닫기 시도...")
                        page.keyboard.press("Escape")
                except:
                    pass
            else:
                print("이미 로그인되어 있는 것으로 보입니다.")

            # 2. 인재 검색 (Talent Search)
            target_url = "https://www.jobkorea.co.kr/Corp/Person/Find"
            print(f"인재검색 페이지 이동: {target_url}")
            page.goto(target_url)
            page.wait_for_load_state('domcontentloaded')
            time.sleep(2)
            
            # 3. 검색 조건 입력 (Search Input)
            print("검색 조건 설정 중...")
            
            # Dropdown: '일치검색' 선택
            # Browser Tool Exploration 결과: Dropdown class '.search-select-type' or '.searchBar .select'
            try:
                # 통합검색/일치검색 드롭다운 열기
                dropdown = page.locator(".search-select-type, .searchBar .select").first
                if dropdown.is_visible():
                    dropdown.click()
                    time.sleep(0.5)
                    # '일치검색' 클릭
                    page.locator("li:has-text('일치검색')").click()
                    print("'일치검색' 모드 선택 완료")
                
                time.sleep(1)
                
                # 키워드 'SQA' 입력 (Exact Match)
                # input#txtKeyword
                keyword_input = page.locator("#txtKeyword")
                keyword_input.click()
                
                # JS Injection for 'SQA'
                page.evaluate(f"document.getElementById('txtKeyword').value = '{SEARCH_KEYWORD_EXACT}'")
                # Enter 키 입력으로 태그 등록 유도
                keyword_input.press("Enter")
                time.sleep(1)
                print(f"키워드 1 입력 완료: {SEARCH_KEYWORD_EXACT}")
                
            except Exception as e:
                print(f"일치검색 설정 실패: {e}")
            
            # 키워드 'AI활용' 입력
            try:
                # JS Injection for 'AI활용'
                page.evaluate(f"document.getElementById('txtKeyword').value = '{SEARCH_KEYWORD_MAIN}'")
                keyword_input.press("Enter")
                time.sleep(1)
                print(f"키워드 2 입력 완료: {SEARCH_KEYWORD_MAIN}")
            except Exception as e:
                print(f"메인 키워드 입력 실패: {e}")
                
            # 검색 버튼 클릭
            # ID: btnKeywordSearch (from instruction)
            print("검색 시작...")
            page.evaluate("document.getElementById('btnKeywordSearch').click()")
            
            # 결과 로딩 대기
            time.sleep(5)
            
            # 4. 데이터 추출 (Data Extraction)
            print("데이터 추출 중...")
            
            # JS 기반 추출 로직 (Instruction v3 따름)
            candidates = page.evaluate("""
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
                        
                        // Heuristic: Name is usually the first link text encountered for an rNo
                        if (!entry.Name) entry.Name = text;
                        else if (text && text !== entry.Name && !entry.Title) entry.Title = text;
                        
                        // Robust Experience Extraction
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
                    
                    return Array.from(grouped.values()).filter(c => c.Name).slice(0, 10);
                }
            """)
            
            print(f"추출된 후보자 수: {len(candidates)}")
            for cand in candidates:
                print(f"- {cand['Name']} / {cand['Title']} / {cand['Experience']}")
            
            # 5. CSV 저장
            if candidates:
                with open(CSV_PATH, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.DictWriter(f, fieldnames=['Name', 'Title', 'Experience', 'Link'])
                    writer.writeheader()
                    writer.writerows(candidates)
                print(f"\nCSV 저장 완료: {CSV_PATH}")
            else:
                print("\n저장할 데이터가 없습니다.")

        except Exception as e:
            print(f"오류 발생: {e}")
            import traceback
            traceback.print_exc()
        finally:
            print("작업 완료. 브라우저 대기 중...")
            # input("Press Enter to close...") # 필요 시 주석 해제

if __name__ == "__main__":
    run()
