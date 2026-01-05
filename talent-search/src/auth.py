import os
import time
from playwright.sync_api import sync_playwright

# Constants
AUTH_FILE = 'auth.json'
LOGIN_URL = 'https://www.jobkorea.co.kr/Login/Login_Tot.asp'

# Credentials (Provided by user)
USER_ID = 'wisewires9'
USER_PW = 'insa5051'

def login_and_save_state(username, password):
    """
    Automates the login process using provided credentials and saves the state.
    """
    with sync_playwright() as p:
        # Launch browser (headless=False so we can see what's happening)
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print(f"Opening login page: {LOGIN_URL}")
        page.goto(LOGIN_URL)

        try:
            # 1. Select 'Corporate Member' (기업회원) tab
            print("Selecting 'Corporate Member' tab...")
            # Use a robust text selector for the tab
            page.click("text=기업회원")
            
            # Small wait to ensure tab switch (if any animation)
            page.wait_for_timeout(500)

            # 2. Fill Credentials
            print(f"Entering credentials for user: {username}")
            page.fill("#M_ID", username)
            page.fill("#M_PWD", password)

            # 3. Click Login
            print("Clicking Login button...")
            # The login button inside the form. Sometines there are multiple, so be specific if needed.
            # Using the class or type usually works.
            page.click("button[type='submit']") 
            # If explicit button class is known: page.click(".btnLogin") 

            # 4. Wait for navigation/redirection
            print("Waiting for login to complete...")
            # Wait for URL to change or specific element to appear
            page.wait_for_url("**/Corp/**", timeout=10000) # Expecting redirection to Corporate Home
            # OR wait for a logout button which confirms login
            # page.wait_for_selector("text=로그아웃", timeout=10000)

            print("Login success detected!")
            
            # 5. Save State
            context.storage_state(path=AUTH_FILE)
            print(f"Successfully saved authentication state to {AUTH_FILE}")

        except Exception as e:
            print(f"Error during auto-login: {e}")
            print("\n[!] Login might have failed or required Captcha.")
            print("Keeping browser open for manual inspection for 10 seconds...")
            page.wait_for_timeout(10000)

        finally:
            browser.close()

if __name__ == "__main__":
    if not os.path.exists(AUTH_FILE):
        print("Auth file not found. Attempting auto-login...")
        login_and_save_state(USER_ID, USER_PW)
    else:
        print(f"Auth file '{AUTH_FILE}' already exists. Setup complete.")
