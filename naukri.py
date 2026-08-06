import os
from playwright.sync_api import sync_playwright

RESUME_PATH = "resume/Venkata_4_YOE+.docx"

if not os.path.exists(RESUME_PATH):
    print("Resume file not found.")
    exit(1)

PROFILE_URL = "https://www.naukri.com/mnjuser/profile"

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        slow_mo=500,
    )

    context = browser.new_context()

    page = context.new_page()

    print("Opening Naukri...")
    page.goto("https://www.naukri.com/nlogin/login")

    print("\nPlease log in manually.")
    print("After logging in, press Enter here...")
    input()

    page.goto(PROFILE_URL)

    page.wait_for_load_state("networkidle")

    upload = page.locator("input[type='file']")

    if upload.count() == 0:
        print("Resume upload control not found.")
        page.screenshot(path="profile.png", full_page=True)
    else:
        upload.first.set_input_files(RESUME_PATH)
        page.wait_for_timeout(5000)
        print("Resume upload attempted.")

    input("Press Enter to close the browser...")
    browser.close()
