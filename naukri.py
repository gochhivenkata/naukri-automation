import os
import sys
from playwright.sync_api import sync_playwright, TimeoutError

EMAIL = os.getenv("NAUKRI_EMAIL")
PASSWORD = os.getenv("NAUKRI_PASSWORD")
RESUME = "resume.pdf"

if not EMAIL or not PASSWORD:
    print("❌ GitHub Secrets are missing.")
    sys.exit(1)

def fill_first(page, selectors, value, field_name):
    for selector in selectors:
        try:
            page.locator(selector).wait_for(timeout=5000)
            page.fill(selector, value)
            print(f"✅ Filled {field_name} using: {selector}")
            return
        except Exception:
            continue
    raise Exception(f"Could not find {field_name} field.")

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-dev-shm-usage"
        ]
    )

    context = browser.new_context(
        viewport={"width": 1366, "height": 768},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
    )

    page = context.new_page()

    try:

        print("Opening Naukri Login Page...")

        page.goto(
            "https://www.naukri.com/nlogin/login",
            wait_until="networkidle",
            timeout=60000
        )

        page.screenshot(path="login_page.png", full_page=True)

        print("Page Title :", page.title())
        print("Current URL:", page.url)

        # Possible email selectors
        email_selectors = [
            "#usernameField",
            "input[type='email']",
            "input[placeholder*='Email']",
            "input[name='email']",
            "input[name='username']"
        ]

        # Possible password selectors
        password_selectors = [
            "#passwordField",
            "input[type='password']",
            "input[name='password']"
        ]

        fill_first(page, email_selectors, EMAIL, "Email")
        fill_first(page, password_selectors, PASSWORD, "Password")

        print("Clicking Login...")

        login_buttons = [
            "button[type='submit']",
            "button.loginButton",
            "button:has-text('Login')"
        ]

        clicked = False

        for btn in login_buttons:
            try:
                page.locator(btn).click(timeout=5000)
                clicked = True
                print(f"✅ Clicked Login using {btn}")
                break
            except Exception:
                pass

        if not clicked:
            raise Exception("Login button not found.")

        page.wait_for_load_state("networkidle")

        page.screenshot(path="after_login.png", full_page=True)

        print("Current URL:", page.url)

        print("Opening Profile Page...")

        page.goto(
            "https://www.naukri.com/mnjuser/profile",
            wait_until="networkidle",
            timeout=60000
        )

        page.screenshot(path="profile.png", full_page=True)

        upload = page.locator("input[type='file']")

        upload.wait_for(timeout=30000)

        upload.set_input_files(RESUME)

        print("✅ Resume Uploaded Successfully!")

        page.wait_for_timeout(8000)

        page.screenshot(path="upload_success.png", full_page=True)

    except TimeoutError as e:

        print("❌ Timeout Error")
        print(e)

        page.screenshot(path="timeout.png", full_page=True)

        with open("page.html", "w", encoding="utf-8") as f:
            f.write(page.content())

        raise

    except Exception as e:

        print("❌ Error:", e)

        page.screenshot(path="error.png", full_page=True)

        with open("page.html", "w", encoding="utf-8") as f:
            f.write(page.content())

        raise

    finally:
        browser.close()
