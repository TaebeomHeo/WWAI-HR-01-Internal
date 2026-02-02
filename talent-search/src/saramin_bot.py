import os
import time
from playwright.sync_api import sync_playwright

# 상수 설정
LOGIN_URL = 'https://www.saramin.co.kr/zf_user/member/companies/login'
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
            page.goto(LOGIN_URL)

            # 3. 로그인 정보 입력
            print("아이디/비밀번호 입력 중...")
            # 사람인 기업회원 로그인 폼 셀렉터 (추정됨, 실행하면서 검증 필요)
            # ID 입력
            page.fill("input[name='id']", USER_ID) 
            # PW 입력
            page.fill("input[name='password']", USER_PW)

            # 4. 로그인 버튼 클릭
            print("로그인 버튼 클릭...")
            # 로그인 버튼 셀렉터 (추정)
            page.click("button.btn_login, button[type='submit']")

            # 5. 로그인 성공 여부 확인
            print("로그인 완료 대기 중...")
            # 로그아웃 버튼이나 메인 대시보드 요소를 기다림
            # 기업회원 메인 페이지 URL 패턴: /zf_user/company-main 등
            page.wait_for_timeout(5000) # 임시로 5초 대기

            print("현재 페이지 URL:", page.url)
            
            # 성공 여부 판단 로직 (예시)
            if "login" not in page.url:
                print("로그인 성공 추정!")
            else:
                print("로그인 실패 또는 추가 인증 필요 확인 요망.")

        except Exception as e:
            print(f"오류 발생: {e}")
        
        finally:
            print("브라우저를 10초간 유지합니다...")
            page.wait_for_timeout(10000)
            browser.close()

if __name__ == "__main__":
    run()
