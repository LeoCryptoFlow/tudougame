import requests
import json
import random

def test_empty_email_register():
    url = "https://aixin.chat/api/agents"
    rand_id = random.randint(1000, 9999)

    print(f"1. Testing register with empty email")
    payload = {
        "email": "",
        "nickname": f"Test Agent {rand_id}",
        "agent_type": "bot",
        "system_prompt": "I am a test agent"
    }

    try:
        r1 = requests.post(url, json=payload, timeout=10)
        print(f"Status 1: {r1.status_code}, Response: {r1.text}")
    except Exception as e:
        print(f"Request 1 failed: {e}")

    print(f"\n2. Testing register with NO email field at all")
    payload2 = {
        "nickname": f"Test Agent {rand_id + 1}",
        "agent_type": "bot",
        "system_prompt": "I am a test agent 2"
    }

    try:
        r2 = requests.post(url, json=payload2, timeout=10)
        print(f"Status 2: {r2.status_code}, Response: {r2.text}")
    except Exception as e:
        print(f"Request 2 failed: {e}")

if __name__ == "__main__":
    test_empty_email_register()
