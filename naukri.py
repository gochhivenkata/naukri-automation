import os
import sys
from playwright.sync_api import sync_playwright

EMAIL = os.getenv("NAUKRI_EMAIL")
PASSWORD = os.getenv("NAUKRI_PASSWORD")

if not EMAIL or not PASSWORD:
    print("❌ Missing NAUKRI_EMAIL or NAUKRI_PASSWORD")
    sys.exit(1)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    context = browser.new_context(
        viewport={"width": 1366, "height": 768}
    )

    page = context.new_page()

    try:
        print("Opening login page...")

        page.goto(
            "https://www.naukri.com/nlogin/login",
            wait_until="domcontentloaded",
            timeout=60000
        )

        print("Title:", page.title())
        print("URL:", page.url)

        page.screenshot(path="login_page.png", full_page=True)

        with open("page.html", "w", encoding="utf-8") as f:
            f.write(page.content())

        if "Access Denied" in page.title():
            print("❌ Access denied by Naukri.")
            print("See login_page.png and page.html for details.")
            sys.exit(1)

        email_box = page.locator("#usernameField")

        if email_box.count() == 0:
            print("❌ Login field not found.")
            sys.exit(1)

        print("✅ Login page loaded successfully.")

    finally:
        browser.close()
