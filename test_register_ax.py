import requests
import json
import random

def test_register():
    url = "https://aixin.chat/api/agents"
    # Or try http://43.135.138.144:3000/api/agents if domain is not working
    
    rand_id = random.randint(1000, 9999)
    email = f"test_{rand_id}@example.com"
    
    print(f"1. Testing send code to {email}")
    send_url = "https://aixin.chat/api/auth/send-code"
    try:
        r1 = requests.post(send_url, json={"email": email}, timeout=10)
        print(f"Status: {r1.status_code}, Response: {r1.text}")
    except Exception as e:
        print(f"Send code failed: {e}")
        return

    # Assuming we can't easily retrieve the verify code, 
    # Let's check our local testing tool output to see how we bypass it or if we can read DB.
    # From earlier messages, it seems email registration is enabled and working, returning 400 '请填写邮箱验证码'.
    # This means the API is up, the code change in `core/identity.js` is active.

if __name__ == "__main__":
    test_register()
