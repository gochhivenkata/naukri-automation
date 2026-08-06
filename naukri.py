import os
from playwright.sync_api import sync_playwright

EMAIL = os.getenv("NAUKRI_EMAIL")
PASSWORD = os.getenv("NAUKRI_PASSWORD")

RESUME = "resume.pdf"


if not EMAIL or not PASSWORD:
    raise Exception("Naukri secrets missing")


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True
    )

    page = browser.new_page()

    print("Opening Naukri...")

    page.goto(
        "https://www.naukri.com/nlogin/login",
        timeout=60000
    )

    page.wait_for_timeout(3000)

    print("Entering login details")

    page.fill(
        "#usernameField",
        EMAIL
    )

    page.fill(
        "#passwordField",
        PASSWORD
    )


    page.click(
        "button[type='submit']"
    )

    page.wait_for_timeout(8000)


    print("Opening profile page")

    page.goto(
        "https://www.naukri.com/mnjuser/profile",
        timeout=60000
    )


    page.wait_for_timeout(5000)


    print("Uploading resume")


    upload = page.locator(
        "input[type='file']"
    )

    upload.set_input_files(
        RESUME
    )


    page.wait_for_timeout(10000)


    print("✅ Resume upload completed")


    browser.close()
