import os
import sys

print("=" * 50)
print("GitHub Actions Environment Variable Debug")
print("=" * 50)

email = os.getenv("NAUKRI_EMAIL")
password = os.getenv("NAUKRI_PASSWORD")

print(f"NAUKRI_EMAIL: {repr(email)}")
print(f"NAUKRI_PASSWORD: {'SET' if password else 'NOT SET'}")

print("\nEnvironment variables containing 'NAUKRI':")
for key, value in os.environ.items():
    if "NAUKRI" in key.upper():
        if "PASSWORD" in key.upper():
            print(f"{key} = ********")
        else:
            print(f"{key} = {value}")

print("=" * 50)

if not email:
    print("❌ ERROR: NAUKRI_EMAIL is not set.")
    sys.exit(1)

if not password:
    print("❌ ERROR: NAUKRI_PASSWORD is not set.")
    sys.exit(1)

print("✅ Both secrets are available.")
