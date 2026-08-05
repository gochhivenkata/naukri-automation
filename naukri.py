from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import getpass
import os
import time


# ==========================
# CONFIGURATION
# ==========================

EMAIL = os.getenv("NAUKRI_EMAIL") or input("Naukri Email: ")
PASSWORD = os.getenv("NAUKRI_PASSWORD") or getpass.getpass("Naukri Password: ")

# Resume path inside GitHub repository
# Example:
# naukri-automation/
# ├── naukri.py
# └── resume/
#     └── Venkata_4_YOE+.docx

RESUME_PATH = "resume/Venkata_4_YOE+.docx"


# ==========================
# CHROME SETUP
# ==========================

options = webdriver.ChromeOptions()

# Required for GitHub Actions
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Optional stability settings
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)


# ==========================
# NAUKRI LOGIN + RESUME UPLOAD
# ==========================

try:

    wait = WebDriverWait(driver, 20)

    print("Opening Naukri login page...")

    driver.get("https://www.naukri.com/nlogin/login")


    # Enter email
    email_box = wait.until(
        EC.presence_of_element_located(
            (By.ID, "usernameField")
        )
    )

    email_box.send_keys(EMAIL)


    # Enter password
    password_box = driver.find_element(
        By.ID,
        "passwordField"
    )

    password_box.send_keys(PASSWORD)


    # Click login button
    login_button = driver.find_element(
        By.XPATH,
        "//button[@type='submit']"
    )

    login_button.click()


    print("Login submitted...")

    time.sleep(5)


    # Open profile page
    driver.get(
        "https://www.naukri.com/mnjuser/profile"
    )


    print("Opening profile page...")


    # Find resume upload input
    upload = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[@type='file']")
        )
    )


    # Upload resume
    upload.send_keys(
        os.path.abspath(RESUME_PATH)
    )


    print("Resume uploaded successfully!")


    time.sleep(5)


except Exception as e:

    print("Automation failed:")
    print(e)


finally:

    driver.quit()
    print("Browser closed.")
