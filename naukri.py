import os
import sys

# Read credentials from GitHub Secrets
EMAIL = os.getenv("venkata.gochhi@gmail.com")
PASSWORD = os.getenv("Ril$54321")

if not EMAIL:
    print("ERROR: NAUKRI_EMAIL is not set.")
    sys.exit(1)

if not PASSWORD:
    print("ERROR: NAUKRI_PASSWORD is not set.")
    sys.exit(1)

# Resume path
RESUME_PATH = os.path.abspath("resume/Venkata_4_YOE+.docx")

if not os.path.exists(RESUME_PATH):
    print(f"ERROR: Resume not found: {RESUME_PATH}")
    sys.exit(1)
