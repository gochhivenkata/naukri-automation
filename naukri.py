from playwright.sync_api import sync_playwright
import os
import time
import glob

# Read credentials from GitHub Secrets / Environment Variables
EMAIL = os.getenv("NAUKRI_EMAIL")
PASSWORD = os.getenv("NAUKRI_PASSWORD")

if not EMAIL or not PASSWORD:
    raise Exception("NAUKRI_EMAIL or NAUKRI_PASSWORD environment variable is missing.")

# Find the resume automatically
resume_files = glob.glob("resume/*.docx")

if not resume_files:
    raise Exception("No resume file found inside the 'resume' folder.")

RESUME_PATH = os.path.abspath(resume_files[0])

print(f"Uploading Resume: {RESUME_PATH}")

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True
    )

    page = browser.new_page()

    # Open Login Page
    page.goto("https://www.naukri.com/nlogin/login", timeout=60000)

    page.fill('input[type="text"]', EMAIL)
    page.fill('input[type="password"]', PASSWORD)

    page.click('button[type="submit"]')

    page.wait_for_load_state("networkidle")

    print("Login Successful")

    # Open Profile Page
    page.goto("https://www.naukri.com/mnjuser/profile", timeout=60000)

    page.wait_for_timeout(5000)

    # Upload Resume
    page.set_input_files(
        'input[type="file"]',
        RESUME_PATH
    )

    print("Resume Uploaded Successfully")

    page.wait_for_timeout(8000)

    browser.close()
