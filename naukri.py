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

# Full path to your resume (include the filename and extension)
RESUME_PATH = "/Users/administrator/Documents/Venkata_4_YOE+.docx"

# Launch Chrome (Selenium Manager will download the correct driver if needed)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

try:
    driver.maximize_window()

    wait = WebDriverWait(driver, 20)

    # Open login page
    driver.get("https://www.naukri.com/nlogin/login")

    # Login
    wait.until(
        EC.presence_of_element_located((By.ID, "usernameField"))
    ).send_keys(EMAIL)

    driver.find_element(By.ID, "passwordField").send_keys(PASSWORD)

    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # Wait for login
    time.sleep(5)

    # Open profile page
    driver.get("https://www.naukri.com/mnjuser/profile")

    # Upload resume
    upload = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
    )

    upload.send_keys(RESUME_PATH)

    print("Resume uploaded successfully.")

    time.sleep(5)

finally:
    driver.quit()
