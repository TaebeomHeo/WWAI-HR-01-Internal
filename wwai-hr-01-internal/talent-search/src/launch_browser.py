from playwright.sync_api import sync_playwright
import time
import os

def launch_persistent_browser():
    print("Launching Persistent Browser on Port 9222...")
    with sync_playwright() as p:
        # Launch with debugging port enabled
        browser = p.chromium.launch(
            headless=False,
            args=['--remote-debugging-port=9222']
        )
        print("Browser launched. Listening on port 9222.")
        print("You can now run other scripts to connect to this browser.")
        print("Press Ctrl+C to close the browser (or kill this process).")
        
        # Keep alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Closing browser...")
            browser.close()

if __name__ == "__main__":
    launch_persistent_browser()
