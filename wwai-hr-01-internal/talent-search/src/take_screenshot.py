from playwright.sync_api import sync_playwright

def take_screenshot():
    try:
        with sync_playwright() as p:
            # Connect to the existing browser on port 9222
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            
            print(f"Contexts found: {len(browser.contexts)}")
            
            target_page = None
            for i, context in enumerate(browser.contexts):
                print(f"Context {i}: {len(context.pages)} pages")
                if context.pages:
                    target_page = context.pages[0]
                    break
            
            if not target_page:
                print("No active pages found in any context.")
                # Fallback: maybe we can get contexts from browser.contexts?
                return

            page = target_page
            print(f"Target page found: {page.url}")

            
            # Bring to front (optional attempt)
            try:
                page.bring_to_front()
            except:
                pass

            screenshot_path = "current_screen.png"
            page.screenshot(path=screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")
            
    except Exception as e:
        print(f"Error taking screenshot: {e}")

if __name__ == "__main__":
    take_screenshot()
