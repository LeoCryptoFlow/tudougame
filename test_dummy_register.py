import requests
import random
import time

BASE_URL = "http://aixin.chat/api"

def test_full_register_flow(email):
    print(f"\n--- Testing registration for dummy email: {email} ---")
    
    # 1. 发送注册请求尝试 (对于 dummy emails，如果是自动注册，这步可以直接调用真正的注册或者是发送验证码)
    # 实际上我们之前修复了 `register` 方法让它绕过虚拟邮箱检查，但由于虚拟邮箱跳过验证是在业务层 `register` 里，现在可以通过 API 发起注册
    
    # 构造注册 payload，由于 routes.js 处理的是 emailCode 所以发送此字段
    register_payload = {
        "email": email,
        "password": "Password123!",
        "nickname": f"Dummy {random.randint(1000, 9999)}",
        "agent_type": "human",
        "emailCode": "123456" # 由于我们的后端对虚拟邮箱 @aixin.dummy 忽略该字段的真实性
    }
    
    try:
        response = requests.post(f"{BASE_URL}/agents", json=register_payload)
        print(f"Status: {response.status_code}")
        print(f"Raw Response: {response.text}")
        try:
            data = response.json()
            if response.status_code == 200 and data.get("ok"):
                print("✅ Dummy email 注册成功！")
            else:
                print("❌ Dummy email 注册失败！")
        except Exception as json_e:
            print(f"Failed to parse JSON: {json_e}")
    except Exception as e:
        print(f"Error registering: {e}")

if __name__ == "__main__":
    # 我们测试一个 @aixin.dummy 邮箱，这是我们业务里定义的虚拟用户邮箱！
    unique_dummy_email = f"user_{int(time.time())}@aixin.dummy"
    test_full_register_flow(unique_dummy_email)
    
    # 也可以测试下同 dummy 的重复问题，虽然现在会返回错误（由于存在唯一约束或已经注册）。
    test_full_register_flow(unique_dummy_email)