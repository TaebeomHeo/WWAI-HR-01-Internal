import os
import time
from playwright.sync_api import sync_playwright
import auth

# Constants
AUTH_FILE = 'auth.json'
TARGET_URL = 'https://www.jobkorea.co.kr/Corp/Main' 
LOGIN_URL = 'https://www.jobkorea.co.kr/Login/Login_Tot.asp'

def run_bot():
    print("Initializing JobKorea Login Bot (Fresh Start)...")

    # 1. Connect to or Launch Browser
    playwright = sync_playwright().start()
    browser = None
    page = None

    try:
        print("Attempting to connect to existing browser on Port 9222...")
        browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
        if browser.contexts:
            page = browser.contexts[0].pages[0]
        else:
            page = browser.contexts[0].new_page()
        print("Connected to existing browser!")
    except Exception:
        print("No existing browser found. Launching new one...")
        browser = playwright.chromium.launch(headless=False, args=['--remote-debugging-port=9222'])
        page = browser.new_page()

    if not page:
        print("Failed to get a page.")
        return

    try:
        # 2. Go to Login Page directly to ensure clean state
        print("Navigating to Login Page...")
        page.goto(LOGIN_URL)
        page.wait_for_load_state("domcontentloaded")

        # 3. Perform Login Logic
        print("Performing Login actions...")
        
        # Check if already logged in?
        if "Login" not in page.url and "login" not in page.url:
            print("It seems we are already logged in (URL does not contain 'Login').")
            # Go to Corporate Home to verify
            page.goto(TARGET_URL)
        else:
            # Login Process
            try:
                # Click 'Corporate Member' tab
                if page.is_visible("text=기업회원"):
                    print("Selecting 'Corporate Member' tab...")
                    page.click("text=기업회원")
                    time.sleep(1)

                # Fill ID
                if page.is_visible("#lb_id"):
                    page.fill("#lb_id", auth.USER_ID)
                elif page.is_visible("input[name='M_ID']"):
                    page.fill("input[name='M_ID']", auth.USER_ID)
                
                # Fill PW
                if page.is_visible("#lb_pw"):
                    page.fill("#lb_pw", auth.USER_PW)
                elif page.is_visible("input[name='M_PWD']"):
                    page.fill("input[name='M_PWD']", auth.USER_PW)

                # Click Login
                print("Clicking Login button...")
                if page.is_visible(".btn_login"):
                    page.click(".btn_login")
                elif page.is_visible("button[type='submit']"):
                    page.click("button[type='submit']")
                else:
                    page.press("body", "Enter")

                print("Login submitted. Waiting for navigation...")
                # Optimize: Rely on Playwright's auto-wait for navigation after click
                # page.wait_for_load_state("domcontentloaded") # Playwright often waits for navigation by default after click
                # time.sleep(3) # Extra grace period - removed for speedup

            except Exception as e:
                print(f"Error during login inputs: {e}")

        # 4. Final Verification
        print("Current URL:", page.url)
        print("="*50)
        print(" LOGIN PROCESS COMPLETE ")
        print("==================================================")

        # --- TALENT SEARCH LOGIC ---
        print("\n[STEP 2] Navigating to Talent Search...")
        
        # Give some time for login redirects to settle
        time.sleep(3) 

        # Robust Navigation with Retry
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Optimize: Use wait_until='domcontentloaded'
                page.goto("https://www.jobkorea.co.kr/Corp/Person/Find/Index", wait_until='domcontentloaded')
                break # Success
            except Exception as nav_err:
                print(f"Navigation attempt {attempt+1} failed: {nav_err}")
                time.sleep(2)
        
        print(f"Current URL after navigation: {page.url}")
        
        print("[STEP 3] Executing 'QA' Exact Match Search...")

        print("  (Optimized navigation and reduced sleeps for faster execution)")

        try:
            # 1. Click "통합검색" (Combined Search)
            print("  - Clicking 'Combined Search'...")
            # Try specific selectors
            if page.is_visible("text=통합검색"):
                page.click("text=통합검색")
            elif page.is_visible(".btn_search_detail"): 
                page.click(".btn_search_detail")
            else:
                print("    (Combined Search button not found, assuming filters are visible)")
            
            time.sleep(1)

            # 2. Check "일치" (Exact Match)
            print("  - Setting 'Exact Match'...")
            if page.is_visible("text=일치"):
                page.click("text=일치")
            else:
                print("    ('Exact Match' checkbox/label not found)")

            # 3. Input "QA" and Enter
            print("  - Inputting 'QA' and Searching...")
            # Target the search input. 
            # Often .ipt_keyword or #dev_SearchText
            page.fill("input[type='text']", "QA") 
            page.press("input[type='text']", "Enter")
            
            print("Search command sent.")
            
            # Wait for results to load (basic visual wait)
            time.sleep(2)
            
            # Bring to front and Screenshot
            try:
                page.bring_to_front()
                page.screenshot(path="search_result.png")
                print("Screenshot saved to search_result.png")
            except Exception as ss_err:
                print(f"Screenshot/Focus error: {ss_err}")

        except Exception as search_err:
            print(f"Search Error: {search_err}")

        print("="*50)
        print(" ACTION COMPLETED: Check Browser for Results ")


    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        print("Script finished. Browser will remain open.")
        # Keep alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Exiting...")

if __name__ == "__main__":
    run_bot()
