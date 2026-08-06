import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

EMAIL = os.getenv("NAUKRI_EMAIL")
PASSWORD = os.getenv("NAUKRI_PASSWORD")
RESUME_PATH = os.path.abspath("resume.pdf")   # Resume in repository

if not EMAIL or not PASSWORD:
    raise Exception("GitHub Secrets are missing.")

print("Starting browser...")

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 30)

try:
    # Open Login Page
    driver.get("https://www.naukri.com/nlogin/login")

    # Login
    wait.until(EC.presence_of_element_located((By.ID, "usernameField"))).send_keys(EMAIL)
    driver.find_element(By.ID, "passwordField").send_keys(PASSWORD)

    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    print("Logged in...")

    # Wait until profile page is available
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@class,'view-profile-wrapper')]")
        )
    )

    # Open profile page
    driver.get("https://www.naukri.com/mnjuser/profile")

    print("Opening profile...")

    # Wait for Upload Resume button
    upload = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//input[@type='file']"
            )
        )
    )

    upload.send_keys(RESUME_PATH)

    print("Uploading resume...")

    time.sleep(10)

    print("✅ Resume uploaded successfully!")

except Exception as e:
    print("Upload failed")
    print(e)
    driver.save_screenshot("error.png")
    raise

finally:
    driver.quit()
