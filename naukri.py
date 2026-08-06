import os
import time
from playwright.sync_api import sync_playwright, TimeoutError


# -----------------------------
# Read Credentials
# -----------------------------
EMAIL = os.getenv("NAUKRI_EMAIL")
PASSWORD = os.getenv("NAUKRI_PASSWORD")

if not EMAIL or not PASSWORD:
    print("❌ Missing Naukri credentials")
    exit(1)


# -----------------------------
# Resume Path
# -----------------------------
RESUME_PATH = "resume/Venkata_4_YOE+.docx"

if not os.path.exists(RESUME_PATH):
    print("❌ Resume file not found")
    exit(1)


# -----------------------------
# Naukri URL
# -----------------------------
LOGIN_URL = "https://www.naukri.com/nlogin/login"


print("=" * 60)
print("Starting Naukri Resume Upload")
print("=" * 60)


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--start-maximized"
        ]
    )


    context = browser.new_context(
        viewport={
            "width": 1366,
            "height": 768
        },

        user_agent=(
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        )
    )


    page = context.new_page()


    try:

        print("\nOpening Naukri Login Page...")

        page.goto(
            LOGIN_URL,
            wait_until="domcontentloaded",
            timeout=60000
        )


        time.sleep(5)


        print("Title :", page.title())
        print("URL   :", page.url)


        html = page.content()


        if "Access Denied" in html:

            print("\n❌ Naukri blocked the request")

            page.screenshot(
                path="login_blocked.png",
                full_page=True
            )

            with open(
                "blocked.html",
                "w",
                encoding="utf-8"
            ) as f:
                f.write(html)

            exit(1)


        # -----------------------------
        # Login
        # -----------------------------

        print("\nEntering username...")


        page.fill(
            "input[type='text']",
            EMAIL
        )


        page.fill(
            "input[type='password']",
            PASSWORD
        )


        page.click(
            "button[type='submit']"
        )


        time.sleep(8)


        print("Current URL:", page.url)


        # -----------------------------
        # Upload Resume
        # -----------------------------

        print("\nOpening profile page...")


        page.goto(
            "https://www.naukri.com/mnjuser/profile",
            wait_until="domcontentloaded",
            timeout=60000
        )


        time.sleep(5)


        print(
            "Profile Page:",
            page.title()
        )


        # Resume upload selector
        upload = page.locator(
            "input[type='file']"
        )


        if upload.count() > 0:

            print("Uploading resume...")

            upload.set_input_files(
                RESUME_PATH
            )

            time.sleep(10)

            print(
                "✅ Resume uploaded successfully"
            )

        else:

            print(
                "⚠ Resume upload button not found"
            )

            page.screenshot(
                path="profile.png"
            )


    except TimeoutError as e:

        print(
            "❌ Timeout Error:",
            e
        )

        page.screenshot(
            path="error.png"
        )


    except Exception as e:

        print(
            "❌ Error:",
            e
        )

        page.screenshot(
            path="exception.png"
        )


    finally:

        browser.close()


print("\nCompleted")
