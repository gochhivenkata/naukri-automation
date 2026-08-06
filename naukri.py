import os
import sys
from playwright.sync_api import sync_playwright, TimeoutError

EMAIL = os.getenv("NAUKRI_EMAIL")
PASSWORD = os.getenv("NAUKRI_PASSWORD")

if not EMAIL or not PASSWORD:
    print("❌ Missing NAUKRI_EMAIL or NAUKRI_PASSWORD")
    sys.exit(1)

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True
    )

    context = browser.new_context(
        viewport={"width": 1366, "height": 768},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
    )

    page = context.new_page()

    try:
        print("=" * 60)
        print("Opening Naukri Login Page...")
        print("=" * 60)

        page.goto(
            "https://www.naukri.com/nlogin/login",
            wait_until="domcontentloaded",
            timeout=60000
        )

        print(f"Title : {page.title()}")
        print(f"URL   : {page.url}")

        # Save screenshot
        page.screenshot(
            path="login_page.png",
            full_page=True
        )

        # Save HTML
        with open("page.html", "w", encoding="utf-8") as f:
            f.write(page.content())

        # Print first part of HTML for debugging
        print("\nFirst 1000 characters of HTML:\n")
        print(page.content()[:1000])

        # Check if blocked
        if "Access Denied" in page.title():
            print("\n❌ Naukri blocked the request.")
            print("Screenshot saved as login_page.png")
            print("HTML saved as page.html")
            sys.exit(1)

        # Wait for email field
        page.wait_for_selector("#usernameField", timeout=10000)

        print("✅ Login page loaded successfully.")

    except TimeoutError:
        print("❌ Timed out waiting for the login page.")

        page.screenshot(
            path="timeout.png",
            full_page=True
        )

        with open("timeout.html", "w", encoding="utf-8") as f:
            f.write(page.content())

    except Exception as e:
        print(f"❌ Error: {e}")

        page.screenshot(
            path="error.png",
            full_page=True
        )

        with open("error.html", "w", encoding="utf-8") as f:
            f.write(page.content())

        raise

    finally:
        browser.close()

print("Script finished.")
