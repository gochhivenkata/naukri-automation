from playwright.sync_api import sync_playwright, TimeoutError
import os
import glob
import sys

# -------------------------
# Read Environment Variables
# -------------------------
EMAIL = os.getenv("NAUKRI_EMAIL")
PASSWORD = os.getenv("NAUKRI_PASSWORD")

if not EMAIL or not PASSWORD:
    print("ERROR: NAUKRI_EMAIL or NAUKRI_PASSWORD is missing.")
    sys.exit(1)

# -------------------------
# Find Resume
# -------------------------
resume_files = glob.glob("resume/*.docx")

if not resume_files:
    print("ERROR: No .docx file found in resume folder.")
    sys.exit(1)

RESUME_PATH = os.path.abspath(resume_files[0])

print("=" * 60)
print("Resume:", RESUME_PATH)
print("=" * 60)

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox"
        ]
    )

    context = browser.new_context(
        viewport={"width": 1366, "height": 768},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
    )

    page = context.new_page()

    try:

        print("Opening Naukri login page...")

        page.goto(
            "https://www.naukri.com/nlogin/login",
            wait_until="domcontentloaded",
            timeout=60000
        )

        print("Title :", page.title())
        print("URL   :", page.url)

        # Save screenshot
        page.screenshot(path="login_page.png", full_page=True)

        # Save HTML
        with open("page.html", "w", encoding="utf-8") as f:
            f.write(page.content())

        page.wait_for_timeout(5000)

        print("Waiting for email field...")

        page.wait_for_selector('input[type="text"]', timeout=30000)

        page.locator('input[type="text"]').first.fill(EMAIL)
        page.locator('input[type="password"]').fill(PASSWORD)

        print("Clicking Login...")

        page.locator('button[type="submit"]').click()

        page.wait_for_load_state("networkidle")

        print("Logged in successfully.")

        print("Opening profile page...")

        page.goto(
            "https://www.naukri.com/mnjuser/profile",
            wait_until="networkidle",
            timeout=60000
        )

        page.wait_for_timeout(5000)

        page.screenshot(path="profile_page.png", full_page=True)

        print("Uploading Resume...")

        page.set_input_files(
            'input[type="file"]',
            RESUME_PATH
        )

        page.wait_for_timeout(10000)

        page.screenshot(path="upload_success.png", full_page=True)

        print("Resume uploaded successfully!")

    except TimeoutError as e:

        print("Timeout Error:", e)

        page.screenshot(path="error_timeout.png", full_page=True)

        with open("error_page.html", "w", encoding="utf-8") as f:
            f.write(page.content())

        raise

    except Exception as e:

        print("Unexpected Error:", e)

        page.screenshot(path="error.png", full_page=True)

        with open("error.html", "w", encoding="utf-8") as f:
            f.write(page.content())

        raise

    finally:

        browser.close()
