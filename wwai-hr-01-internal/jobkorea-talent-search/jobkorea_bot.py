import os
import time
from playwright.sync_api import sync_playwright

# 상수 설정
JOBKOREA_MAIN_URL = 'https://www.jobkorea.co.kr/'
LOGIN_URL = 'https://www.jobkorea.co.kr/Login/Login_Tot.asp'
USER_ID = 'wisewires9'  # 기존 crawler.js 참조
USER_PW = 'insa5051'    # 기존 crawler.js 참조

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
            # 2. 잡코리아 이동
            # 이미 잡코리아에 접속해 있는지 확인
            if "jobkorea.co.kr" in page.url:
                print(f"이미 잡코리아 페이지입니다: {page.url}")
            else:
                print(f"잡코리아 메인으로 이동 중: {JOBKOREA_MAIN_URL}")
                page.goto(JOBKOREA_MAIN_URL)
                page.wait_for_load_state("networkidle")

            # 3. 로그인 여부 확인 (헤더의 로그아웃 버튼 등으로 확인 가능하나, 단순하게 로그인 페이지 이동 시도로 판단)
            # 로그인 페이지로 바로 이동
            print("로그인 페이지 이동 중...")
            page.goto(LOGIN_URL)
            page.wait_for_load_state("networkidle")
            
            # URL이 메인으로 리다이렉트되거나 로그인 페이지가 아니라면 이미 로그인된 상태일 수 있음
            if "Login" not in page.url and "login" not in page.url:
                 print("이미 로그인 된 상태로 보입니다 (리다이렉트 됨).")
            else:
                print("로그인 프로세스 시작...")

                # 4. 기업회원 탭 클릭
                # 잡코리아는 '개인회원' / '기업회원' 탭이 나뉘어 있음
                # 선택자: #lb_id (기업회원 탭을 누르면 나오는 ID 입력창이 #lb_id 인지, 탭 버튼이 따로 있는지 확인 필요)
                # 보통 기업회원 탭: li.searchType02 button or a
                
                # 우선 기업회원 탭을 찾아서 클릭 (필요한 경우)
                try:
                    # 기업회원 탭 (비즈니스 URL로 이동하는 경우도 있지만, 통합 로그인 페이지에서는 탭 전환)
                    # 통합 로그인 페이지에서 기업회원 탭 찾기
                    # (실제 DOM 구조 확인이 어려우므로 일반적인 텍스트 기반 검색 시도)
                    corp_tab = page.get_by_text("기업회원", exact=True)
                    if corp_tab.count() > 0:
                        print("기업회원 탭 클릭...")
                        corp_tab.click()
                        time.sleep(1) # UI 변경 대기
                except Exception as e:
                    print(f"기업회원 탭 처리 중 예외 (무시 가능): {e}")

                # 5. 아이디/비밀번호 입력
                print("아이디/비밀번호 입력 중...")
                
                # 기업회원 ID selector: #lb_id 또는 #M_ID
                # 기업회원 PW selector: #lb_pw 또는 #M_PWD
                # crawler.js 참조: input[name="M_ID"], #lb_id
                
                if page.is_visible("#lb_id"):
                    page.fill("#lb_id", USER_ID)
                elif page.is_visible("input[name='M_ID']"):
                     page.fill("input[name='M_ID']", USER_ID)
                else:
                    print("ID 입력 필드를 찾을 수 없습니다. 수동으로 입력해주세요.")
                
                if page.is_visible("#lb_pw"):
                    page.fill("#lb_pw", USER_PW)
                elif page.is_visible("input[name='M_PWD']"):
                    page.fill("input[name='M_PWD']", USER_PW)
                else:
                    print("PW 입력 필드를 찾을 수 없습니다.")

                # 6. 로그인 버튼 클릭
                print("로그인 버튼 클릭...")
                # button.btn_login or input[type=submit]
                if page.is_visible(".btn_login"):
                    page.click(".btn_login")
                else:
                    page.press("body", "Enter") # 엔터키 시도

                # 7. 로그인 완료 대기
                print("로그인 완료 대기 (5초)...")
                time.sleep(5)
                
                # 현재 URL 체크
                print(f"현재 URL: {page.url}")

            # 8. 종료 전 대기
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
            input("종료하려면 Enter...")
            if browser:
                browser.close()

if __name__ == "__main__":
    run()
