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

                    # 주소 추출 (Network Interception & JSON Parsing)
                    address = ""
                    matched_response_data = {}

                    # 페이지 이동 전/후에 발생하는 네트워크 응답을 포착하기 위해 로직 수정 필요하지만,
                    # 여기서는 간단히 page의 request/response 이벤트를 활용하기 어렵고(이미 로드됨),
                    # 리로드하거나, 앞단에서 리스너를 등록해야 함.
                    # 구조상 loop 안에서 매번 리스너를 등록/해제하는 것이 안전함.

                    def handle_response(response):
                        nonlocal address
                        try:
                            # Content-Type 느슨한 체크
                            ctype = response.headers.get("content-type", "").lower()
                            if "json" in ctype:
                                # URL 필터링 (이력서 정보 관련)
                                # data.json? ... 형태일 수도 있음
                                
                                try:
                                    data = response.json()
                                except:
                                    return

                                import json
                                json_str = json.dumps(data, ensure_ascii=False)
                                
                                # 디버깅: JSON 키 로깅 (첫 번째 사람만)
                                if cand == basic_candidates[0] and len(json_str) > 100:
                                    print(f"[DEBUG] JSON Response from {response.url} (Type: {ctype})")
                                    # 너무 기니까 일부만 출력하거나 키만 출력
                                    if isinstance(data, dict):
                                        print(f"Keys: {list(data.keys())}")
                                        if "result" in data:
                                            print(f"Result Keys: {list(data['result'].keys())}")
                                
                                # 키워드 검색
                                if "address" in json_str or "region" in json_str or "addr" in json_str:
                                    # 실제 구조 파싱 시도 (예상: data.result.address)
                                    # 만약 'result' 안에 있다면
                                    target_dict = data
                                    if "result" in data and isinstance(data["result"], dict):
                                        target_dict = data["result"]
                                    
                                    # 가능한 키들 확인
                                    for key in ["address", "addr", "region", "area", "loc"]:
                                        val = target_dict.get(key)
                                        if val and isinstance(val, str) and "제안 수락" not in val:
                                            address = val
                                            print(f"Network에서 주소 발견 ({key}): {address}")
                                            break
                        except Exception as e:
                            # print(f"Network handler error: {e}")
                            pass

                    # 리스너 등록
                    page.on("response", handle_response)
                    
                    # 이미 페이지가 로드된 상태라면 리로드가 필요할 수 있음.
                    # 또는 앞서 goto 하기 전에 등록했어야 함.
                    # 현재 구조에서는 goto 직전에 등록하는 것이 좋으므로,
                    # 이 블록을 goto 위로 옮기거나, 페이지를 리로드함.
                    page.reload() 
                    page.wait_for_load_state('domcontentloaded')
                    time.sleep(2)
                    
                    # 리스너 해제
                    page.remove_listener("response", handle_response)

                    # Shadow DOM Host 확인 (User provided selector) -> 혹시 텍스트가 있을지 확인
                    try:
                        host_selector = "body > div.EmptyLayout_empty-layout__wDWQf > div > div > main > div.layout_main__content__KStXP > div > div.ave9acc8e > div.av7f6f73a.ApplicantViewContent_gray__urLj5.ApplicantViewContent_center__fzGwA > div.av372e2e1.avf7a1d95 > div"
                        # 만약 Host Element의 textContent에 주소가 포함되어 있다면?
                        if not address and page.is_visible(host_selector):
                            host_text = page.inner_text(host_selector)
                            if "서울" in host_text or "경기" in host_text:
                                print("Shadow Host 내부 텍스트에서 지역명 발견")
                                # 간단한 추출 로직 (정규식 등) 필요하나 일단 전체 저장
                                # address = host_text 
                                pass
                    except:
                        pass
                    
                    if not address:
                         print("Network 및 Host Text에서도 주소 확인 실패")

                    cand['address'] = address
                    cand['revisit_url'] = detail_url
                    final_candidates.append(cand)
                    
                    time.sleep(1)
                    
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
