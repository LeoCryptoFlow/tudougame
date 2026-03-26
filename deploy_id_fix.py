import requests

GITHUB_RAW_URL = "https://raw.githubusercontent.com/LeoCryptoFlow/tudougame/main/deploy_update.py"

print("Deploying identity.js fix...")

try:
    with open("aixin/server/src/core/identity.js", "r") as f:
        content = f.read()
    print("identity.js read successfully.")
except Exception as e:
    print(f"Error reading identity.js: {e}")

