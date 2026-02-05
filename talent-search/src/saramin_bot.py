import os
import time
import csv
from datetime import datetime
from playwright.sync_api import sync_playwright

# 상수 설정
LOGIN_URL = 'https://www.saramin.co.kr/zf_user/auth'
SEARCH_URL = 'https://www.saramin.co.kr/zf_user/memcom/talent-pool/main/search'
USER_ID = 'wisewires' 
USER_PW = 'insa5051'

def run():
    with sync_playwright() as p:
        # 1. 브라우저 실행 (Headless=False로 설정하여 육안 확인)
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        try:
            # 2. 로그인 페이지 이동
            print(f"로그인 페이지로 이동 중: {LOGIN_URL}")
            page.goto(LOGIN_URL, timeout=60000)

            # 3. 기업회원 탭 클릭
            print("기업회원 탭 클릭...")
            page.click('.btn_tab.t_com')

            # 4. 로그인 정보 입력
            print("아이디/비밀번호 입력 중...")
            page.fill("#id", USER_ID) 
            page.fill("#password", USER_PW)

            # 5. 로그인 버튼 클릭
            print("로그인 버튼 클릭...")
            page.click('.btn_login')
            
            # 페이지 이동 대기
            page.wait_for_load_state('networkidle')

            # 6. 인재풀 검색 페이지 이동 (로그인 후 리다이렉트가 다를 수 있음)
            print(f"인재풀 검색 페이지로 이동 중: {SEARCH_URL}")
            page.goto(SEARCH_URL)
            page.wait_for_selector('.talent_header', timeout=10000)

            # 7. 검색 조건 초기화
            if page.is_visible('button.btn_reset'):
                print("검색 조건 초기화...")
                page.click('button.btn_reset')
            
            # 검색 패널 열기 (필요시)
            if not page.is_visible('div.search_default'):
                page.click('#app > div.talent_header > div > div > div.btn_search_history_wrap > button')

            # 8. OR 키워드 입력 ("개발") - JS Injection
            print("OR 키워드 '개발' 입력 중...")
            page.click('div.search_default input.search_input.result')
            page.wait_for_selector('.search_detail input.search_input')
            
            page.evaluate("""
                () => {
                    const input = document.querySelector(".search_detail input.search_input");
                    input.value = "개발";
                    input.dispatchEvent(new Event("input", {bubbles:true}));
                    
                    const exactMatch = document.querySelector("#keywordSearch");
                    if (exactMatch) {
                        exactMatch.checked = true; // Exact Match ON
                        exactMatch.dispatchEvent(new Event("change", {bubbles: true}));
                    }
                    
                    const e = new KeyboardEvent("keydown", {bubbles: true, cancelable: true, key: "Enter", code: "Enter", keyCode: 13});
                    input.dispatchEvent(e);
                }
            """)
            time.sleep(1) # 입력 처리 대기

            # 9. AND 키워드 입력 ("금융", "자동차") - JS Injection
            # 9-1. 금융
            print("AND 키워드 '금융' 입력 중...")
            page.click('div.search_word_include input.search_input.result')
            page.wait_for_selector('.search_detail input.search_input')
            
            page.evaluate("""
                () => {
                    const input = document.querySelector(".search_detail input.search_input");
                    input.value = "금융";
                    input.dispatchEvent(new Event("input", {bubbles:true}));
                    
                    const exactMatch = document.querySelector("#keywordSearch");
                    if (exactMatch) {
                        exactMatch.checked = false; // Exact Match OFF (Contains)
                        exactMatch.dispatchEvent(new Event("change", {bubbles: true}));
                    }
                    
                    const e = new KeyboardEvent("keydown", {bubbles: true, cancelable: true, key: "Enter", code: "Enter", keyCode: 13});
                    input.dispatchEvent(e);
                }
            """)
            time.sleep(1)

            # 9-2. 자동차 (AND 입력창을 다시 클릭 후 입력)
            print("AND 키워드 '자동차' 입력 중...")
            # 팝업이 닫혔을 수 있으므로 다시 클릭
            page.click('div.search_word_include input.search_input.result') 
            # 이미 열려있어도 상관없음, 확실히 하기 위함
            
            page.evaluate("""
                () => {
                    const input = document.querySelector(".search_detail input.search_input");
                    if (input) {
                        input.value = "자동차";
                        input.dispatchEvent(new Event("input", {bubbles:true}));
                        
                        const exactMatch = document.querySelector("#keywordSearch");
                        if (exactMatch) {
                            exactMatch.checked = false; // Exact Match OFF
                            exactMatch.dispatchEvent(new Event("change", {bubbles: true}));
                        }
                        
                        const e = new KeyboardEvent("keydown", {bubbles: true, cancelable: true, key: "Enter", code: "Enter", keyCode: 13});
                        input.dispatchEvent(e);
                    }
                }
            """)
            time.sleep(1)

            # 10. 검색 실행
            print("검색 실행 중...")
            page.click('#search_btn')
            
            # 결과 로딩 대기
            page.wait_for_selector('.talent_list_item', timeout=10000)
            time.sleep(2) # 확실한 로딩을 위해 잠시 대기

            # 11. 결과 추출
            print("결과 추출 중...")
            candidates = page.evaluate("""
                () => {
                    const listItems = Array.from(document.querySelectorAll('.talent_list_item'));
                    // Focus 영역도 포함될 수 있으므로 중복 제거 등을 고려해야 하나, 
                    // 간단히 상위 10개 추출
                    
                    return listItems.slice(0, 10).map(item => {
                        return {
                            name: item.querySelector('.name')?.innerText.trim() || "",
                            job_tit: item.querySelector('.job_tit')?.innerText.trim() || "",
                            career: item.querySelector('.career')?.innerText.trim() || "",
                            info: item.querySelector('.info')?.innerText.trim() || "",
                            residx: item.querySelector('.check_area')?.getAttribute('residx') || ""
                        };
                    });
                }
            """)
            
            print(f"추출된 후보자 수: {len(candidates)}")

            # 12. CSV 저장
            today_str = datetime.now().strftime("%Y-%m-%d")
            output_dir = 'talent-search/candidate/saramin'
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, f'candidate_list_{today_str}_saramin.csv')
            
            print(f"CSV 저장 중: {output_file}")
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Name', 'Job_Title', 'Career', 'Info', 'Revisit_URL'])
                
                for c in candidates:
                    # URL 생성 규칙 적용
                    revisit_url = f"https://hiring.saramin.co.kr/applicant-view/position/resume/{c['residx']}"
                    writer.writerow([c['name'], c['job_tit'], c['career'], c['info'], revisit_url])
            
            print("완료!")

        except Exception as e:
            print(f"오류 발생: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            print("브라우저를 종료합니다.")
            browser.close()

if __name__ == "__main__":
    run()
