import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

class JobKoreaCrawler:
    def __init__(self):
        self.driver = None
        self.setup_driver()

    def setup_driver(self):
        options = webdriver.ChromeOptions()
        # Headful mode so we can see what's happening
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def login(self, user_id, user_pw):
        print("Attempting to log in...")
        try:
            # Click the login link if we are not on the login page yet
            # Generic guess for login button on main page if needed, but we are redirected usually.
            
            # Wait for ID input to be visible
            # Common selectors for OK/JobKorea: #lb_id, #id, #M_ID
            wait = WebDriverWait(self.driver, 10)
            
            # Try to find the ID input
            id_input = None
            try:
                 id_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='M_ID'], input#lb_id, input#id")))
            except:
                print("Could not find standard ID input. Trying fallback...")
            
            if id_input:
                id_input.clear()
                id_input.send_keys(user_id)
                
                pw_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='M_PWD'], input#lb_pw, input#pwd")
                pw_input.clear()
                pw_input.send_keys(user_pw)
                pw_input.send_keys(Keys.RETURN)
                
                print("Credentials submitted. Waiting for navigation...")
                time.sleep(5) # Wait for login processing
            else:
                print("Could not automate login. Please login manually.")
                input("Press Enter after you have logged in manually...")
                
        except Exception as e:
            print(f"Login automation failed: {e}")
            print("Please login manually.")
            input("Press Enter after you have logged in manually...")

    def run(self, target_url):
        try:
            print(f"Navigating to: {target_url}")
            self.driver.get(target_url)
            
            # Check for redirect to login
            if "Login" in self.driver.current_url or "login" in self.driver.current_url:
                # Use provided credentials
                self.login("wisewires9", "insa5051")
            
            # Check if we are back on the target list
            if "Applicant/list" not in self.driver.current_url:
                 self.driver.get(target_url)
                 time.sleep(3)

            # Wait for list to load
            print("Waiting for applicant list to load...")
            time.sleep(3) 
            
            self.extract_data()
            
        except Exception as e:
            print(f"An error occurred: {e}")
            self.driver.save_screenshot("debug_error.png")
            with open("debug_source.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
        finally:
            if self.driver:
                self.driver.quit()

    def extract_data(self):
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        
        candidates = []
        
        # Attempt: Look for table rows
        tables = soup.find_all('table')
        print(f"Found {len(tables)} tables.")
        
        if tables:
            # Try to find the biggest table which is likely the list
            # Or iterate all tables
            target_table = max(tables, key=lambda t: len(t.find_all('tr')))
            rows = target_table.find_all('tr')
            
            for row in rows:
                cols = row.find_all(['td', 'th'])
                cols_text = [ele.get_text(strip=True) for ele in cols]
                # Filter out empty or header-only rows if needed
                if len(cols_text) > 2: 
                    candidates.append(cols_text)
                    
        if candidates:
            print("\n" + "="*50)
            print(f"Extracted {len(candidates)} Candidates:")
            print("="*50)
            for idx, candidate in enumerate(candidates, 1):
                # Print first 5 columns to avoid clutter
                print(f"{idx}. {candidate[:5]}") 
            print("="*50 + "\n")

            df = pd.DataFrame(candidates)
            output_file = "jobkorea_applicants.xlsx"
            df.to_excel(output_file, index=False)
            print(f"Successfully saved {len(candidates)} rows to {output_file}")
        else:
            print("No candidate data extracted. Please check debug_source.html.")
            with open("debug_source.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)

if __name__ == "__main__":
    target_url = "https://www.jobkorea.co.kr/Corp/Applicant/list?GI_No=50027324"
    crawler = JobKoreaCrawler()
    crawler.run(target_url)
