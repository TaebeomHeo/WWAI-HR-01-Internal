import os
import time
from playwright.sync_api import sync_playwright

# 상수 설정
LOGIN_URL = 'https://www.saramin.co.kr/zf_user/auth'
USER_ID = 'wisewires'
USER_PW = 'insa5051'

def run():
    with sync_playwright() as p:
        browser = None
        try:
            # 1. 기존 브라우저 연결 시도 (CDP)
            print("기존 브라우저 연결 시도 (Port 9222)...")
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            print("기존 브라우저 연결 성공!")
            # 기존 페이지가 있으면 사용, 없으면 새로 생성
            if browser.contexts and browser.contexts[0].pages:
                page = browser.contexts[0].pages[0]
            else:
                context = browser.contexts[0]
                page = context.new_page()
        except Exception as e:
            print(f"기존 브라우저 연결 실패: {e}")
            print("새 브라우저를 실행합니다...")
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

        try:
            # 2. 로그인 여부 확인 및 로그인 수행
            if "hiring.saramin.co.kr" in page.url:
                print(f"이미 로그인 된 상태입니다: {page.url}")
            else:
                print(f"로그인 페이지로 이동 중: {LOGIN_URL}")
                page.goto(LOGIN_URL)
                page.wait_for_load_state("networkidle")

                # 3. 기업회원 탭 클릭
                print("기업회원 탭 클릭...")
                try:
                    page.click(".btn_tab.t_com", timeout=3000)
                except Exception:
                    print("기업회원 탭을 찾을 수 없거나 이미 활성화 상태일 수 있습니다.")

                # 4. 로그인 정보 입력
                print("아이디/비밀번호 입력 중...")
                # ID 입력
                page.fill("#id", USER_ID) 
                # PW 입력
                page.fill("#password", USER_PW)

                # 5. 로그인 버튼 클릭
                print("로그인 버튼 클릭...")
                page.click(".btn_login")

                # 6. 로그인 성공 여부 확인
                print("로그인 완료 대기 중...")
                
                # URL 변경 대기
                try:
                    page.wait_for_url("**/hiring.saramin.co.kr/**", timeout=10000)
                    print("로그인 성공! (URL 확인됨)")
                except:
                    print("URL 변경 감지 실패, 현재 URL:", page.url)

            # 7. 인재풀 검색 페이지로 이동 (사용자 제공 Direct URL)
            # URL에 "talent-pool" 등이 포함되어 있지 않으면 이동
            if "talent-pool" not in page.url and "search" not in page.url:
                print("인재풀 검색 페이지로 이동 중 (Direct URL)...")
                SEARCH_URL = "https://www.saramin.co.kr/zf_user/memcom/talent-pool/main/search"
                page.goto(SEARCH_URL)
                page.wait_for_load_state("networkidle")
                print("페이지 이동 완료.")
            else:
                print("이미 인재풀 검색 관련 페이지에 있습니다.")

            # 8. 검색 로직 수행
            print("검색 로직 수행 중...")
            
            # 8-1. 기본 키워드 입력 (SQA)
            print("기본 키워드 'SQA' 입력...")
            page.fill(".search_default input.search_input", "SQA")
            page.press(".search_default input.search_input", "Enter")
            page.wait_for_load_state("networkidle")
            
            # 8-2. 정확히 일치 (Exact Match) 설정
            print("정확히 일치 옵션 확인 중...")
            try:
                # 체크박스 상태 확인
                is_exact_checked = page.is_checked("#keywordSearch")
                if not is_exact_checked:
                    print("'정확히 일치' 옵션 활성화...")
                    page.click("label[for='keywordSearch']")
                    page.wait_for_load_state("networkidle")
                else:
                    print("'정확히 일치' 옵션이 이미 활성화되어 있습니다.")
            except Exception as e:
                print(f"정확히 일치 옵션 설정 실패: {e}")

            # 8-3. 포함 검색어 (AND 조건) 입력
            print("포함 검색어 '금융', '개발' 입력...")
            # 입력창이 다시 로드되었을 수 있으므로 대기
            page.wait_for_selector(".search_word_include input.search_input", state="visible")
            
            # 키워드 순차 입력 (엔터로 구분)
            keywords = ["금융", "개발"]
            for keyword in keywords:
                page.type(".search_word_include input.search_input", keyword)
                page.press(".search_word_include input.search_input", "Enter")
                time.sleep(0.5) # 입력 간 약간의 딜레이
            
            # 검색 버튼 클릭 (확실한 반영을 위해)
            print("최종 검색 버튼 클릭...")
            page.click(".btn_search")
            page.wait_for_load_state("networkidle")
            print("검색 완료.")

            
            # 사용자 확인을 위해 대기 (자동 종료 방지)
            print("=========================================")
            print("  [안내] 브라우저가 실행 중입니다.")
            print("  스크립트를 종료하려면 터미널에서 Enter 키를 누르세요.")
            print("=========================================")
            input() 
            
            print("브라우저를 종료합니다...")
            browser.close()

        except Exception as e:
            print(f"오류 발생: {e}")
            import traceback
            traceback.print_exc()
            print("=========================================")
            print("  [오류] 실행 중 에러가 발생했습니다.")
            print("  브라우저 상태를 확인하세요. 종료하려면 Enter를 누르세요.")
            print("=========================================")
            input()
            # 오류 발생 시에도 브라우저는 닫지 않거나, 사용자 입력 후 닫음
            if browser:
                browser.close()
        
        finally:
            # finally에서는 닫지 않음 (위에서 처리)
            pass

if __name__ == "__main__":
    run()
