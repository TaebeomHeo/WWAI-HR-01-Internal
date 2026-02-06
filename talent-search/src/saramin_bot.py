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
    # 사용자 데이터 디렉토리 설정 (로그인 세션 유지용)
    user_data_dir = os.path.join(os.getcwd(), 'playwright_user_data')
    os.makedirs(user_data_dir, exist_ok=True)

    with sync_playwright() as p:
        # 1. 브라우저 실행 (Persistent Context 사용)
        print(f"사용자 데이터 디렉토리: {user_data_dir}")
        context = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            viewport={'width': 1280, 'height': 1024} # 뷰포트 고정 추천
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
            
            print("페이지 로딩 대기 중... (2차 인증이 필요한 경우 브라우저에서 직접 완료해주세요. 완료될 때까지 계속 기다립니다.)")
            page.wait_for_selector('.talent_header', timeout=0)

            # 7. 검색 조건 초기화
            if page.is_visible('button.btn_reset'):
                print("검색 조건 초기화...")
                page.click('button.btn_reset')
            
            # 검색 패널 열기 (필요시)
            if not page.is_visible('div.search_default'):
                page.click('#app > div.talent_header > div > div > div.btn_search_history_wrap > button')

            # 8. OR 키워드 입력 ("개발")
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
                }
            """)
            
            # 텍스트 입력창 클릭 후 Enter 입력
            page.click('.search_detail input.search_input')
            page.press('.search_detail input.search_input', 'Enter')
            time.sleep(1) 

            # 9. AND 키워드 입력 ("금융")
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
                        exactMatch.checked = false; // Exact Match OFF
                        exactMatch.dispatchEvent(new Event("change", {bubbles: true}));
                    }
                }
            """)
            
            # 텍스트 입력창 클릭 후 Enter 입력 (사용자 요청)
            page.click('.search_detail input.search_input')
            page.press('.search_detail input.search_input', 'Enter')
            time.sleep(1)

            # 9-2. 자동차 ("자동차")
            print("AND 키워드 '자동차' 입력 중...")
            page.click('div.search_word_include input.search_input.result') 
            
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
                    }
                }
            """)
            
            # 텍스트 입력창 클릭 후 Enter 입력 (사용자 요청)
            page.click('.search_detail input.search_input')
            page.press('.search_detail input.search_input', 'Enter')
            time.sleep(1)

            # 10. 검색 실행 (동적 업데이트되므로 버튼 클릭 불필요)
            print("검색 결과 업데이트 대기 중...")
            # page.click('#search_btn', force=True) # 삭제
            
            # 결과 로딩 대기 (동적 로딩 시간을 고려하여 대기)
            # 확실한 업데이트를 위해 충분한 대기 시간 부여
            time.sleep(5) 
            # page.wait_for_load_state('networkidle') # 필요시 활성화
            page.wait_for_selector('.talent_list_item', timeout=10000)
            time.sleep(2) 

            # 11. 결과 추출
            print("결과 추출 중...")
            
            # 리스트에서 기본 정보 추출
            basic_candidates = page.evaluate("""
                () => {
                    const listItems = Array.from(document.querySelectorAll('.talent_list_item'));
                    
                    return listItems.slice(0, 10).map(item => {
                        const personInfo = item.querySelector('.personal_info');
                        const name = personInfo?.querySelector('.name')?.innerText.trim() || "";
                        const genderAge = personInfo?.querySelector('.gender_age')?.innerText.trim() || "";
                        const careerAll = personInfo?.querySelector('.career_all')?.innerText.trim() || "";
                        const residx = item.querySelector('.check_area')?.getAttribute('residx') || "";
                        
                        // 기존 Job Title, Career 정보 등도 일단 가져오되, 요구사항에 맞춰 정리
                        // 여기서는 리스트상의 요약정보를 저장
                        return {
                            name: name,
                            gender_age: genderAge,
                            career_all: careerAll,
                            residx: residx
                        };
                    });
                }
            """)
            
            print(f"1차 추출 및 상세 페이지 방문 (총 {len(basic_candidates)}명)...")
            
            final_candidates = []
            
            # 상세 페이지 방문하여 주소 추출
            for cand in basic_candidates:
                if not cand['residx']:
                    continue
                    
                # React Detail URL
                detail_url = f"https://hiring.saramin.co.kr/applicant-view/position/resume/{cand['residx']}"
                print(f"상세 페이지 이동 중: {cand['name']} ({detail_url})")
                
                try:
                    # 상세 페이지로 이동
                    page.goto(detail_url)
                    page.wait_for_load_state('domcontentloaded')
                    time.sleep(2) 

                    # 주소 추출 (DOM Text Analysis)
                    # 사용자 피드백: "인쇄 미리보기 화면이 나타날떄까지 3-5초 기다린 후, div를 dump해서 보면 되지 않을까?"
                    print("페이지 렌더링 대기 (5초)...")
                    time.sleep(5)
                    
                    # 1. Body Text 전체 스캔
                    body_text = page.inner_text("body")
                    
                    address = ""
                    # "주소", "거주지" 키워드 주변 텍스트 탐색
                    # 예: "주소 : 서울특별시 ..." 또는 "거주지 : 경기도 ..."
                    # 정규식으로 패턴 매칭 시도
                    import re
                    
                    # 패턴 1: '주소' 또는 '거주지' 뒤에 나오는 텍스트
                    # (줄바꿈이 있을 수 있으므로 주의)
                    match = re.search(r"(주소|거주지)\s*[:]?\s*([^\n]+)", body_text)
                    if match:
                        found_addr = match.group(2).strip()
                        # 너무 긴 문장은 오탐일 수 있으므로 길이 체크
                        if len(found_addr) < 50:
                            address = found_addr
                            print(f"DOM 텍스트에서 주소 발견: {address}")
                    
                    # 패턴 2: 만약 키워드가 없다면, body text에서 '시'/'도'/'구'/'군'이 포함된 짧은 라인을 찾을 수도 있음
                    # (오탐 가능성이 높으므로 일단 보류하고, 키워드가 없다면 전체 덤프에서 확인)
                    
                    if not address:
                        print("주소/거주지 키워드를 Text에서 찾을 수 없습니다.")
                        # 첫 번째 후보자에 대해서만 HTML 덤프 저장
                        if cand == basic_candidates[0]:
                             debug_html_path = "debug_saramin_resume.html"
                             with open(debug_html_path, "w", encoding="utf-8") as f:
                                 f.write(page.content())
                             print(f"[DEBUG] HTML 덤프 저장 완료: {debug_html_path}")
                        
                        cand['address'] = ""

                    cand['revisit_url'] = detail_url
                    final_candidates.append(cand)
                    
                    # 결과 확인을 위해 잠시 대기
                    # time.sleep(1)
                    
                except Exception as e:
                    print(f"상세 페이지 처리 중 오류: {e}")
                    cand['address'] = "Error"
                    cand['revisit_url'] = detail_url
                    final_candidates.append(cand)

            # 12. CSV 저장
            today_str = datetime.now().strftime("%Y-%m-%d")
            output_dir = 'talent-search/candidate/saramin'
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, f'candidate_list_{today_str}_saramin.csv')
            
            print(f"CSV 저장 중: {output_file}")
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # 헤더 변경: Name, Gender_Age, Total_Career, Address, Revisit_URL
                writer.writerow(['Name', 'Gender_Age', 'Total_Career', 'Address', 'Revisit_URL'])
                
                for c in final_candidates:
                    writer.writerow([c['name'], c['gender_age'], c['career_all'], c.get('address', ''), c['revisit_url']])
            
            print("완료!")

        except Exception as e:
            print(f"오류 발생: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            print("작업 완료. 브라우저는 열린 상태로 유지됩니다.")
            # context.close()  # 브라우저 유지
            input("브라우저를 종료하려면 Enter를 누르세요...") # 스크립트 종료 방지

if __name__ == "__main__":
    run()
