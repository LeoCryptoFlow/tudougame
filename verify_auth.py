# -*- coding: utf-8 -*-
"""验证认证修复是否生效"""
import urllib.request
import json
import ssl
import time

# 忽略SSL验证（如果证书有问题）
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

BASE = "https://aixin.chat/api"
results = []

def test(name, url, method="GET", data=None):
    try:
        req = urllib.request.Request(url, method=method)
        if data:
            req.add_header('Content-Type', 'application/json')
            req.data = json.dumps(data).encode()
        resp = urllib.request.urlopen(req, context=ctx, timeout=10)
        body = resp.read().decode()
        results.append(f"✅ {name}: HTTP {resp.status} → {body[:150]}")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        results.append(f"🔒 {name}: HTTP {e.code} → {body[:150]}")
    except Exception as e:
        results.append(f"❌ {name}: {e}")

# 测试1: 无token访问受保护接口 → 应返回401
test("无token查未读消息", f"{BASE}/messages/test-user/unread")

# 测试2: 登录接口 → 错误密码应返回错误
test("错误密码登录", f"{BASE}/auth/login", "POST", {"axId": "test", "password": "wrong"})

# 测试3: 公开接口 → 应返回200
test("公开接口agents", f"{BASE}/agents")

# 测试4: 无token发消息 → 应返回401
test("无token发消息", f"{BASE}/messages", "POST", {"from": "fake", "to": "victim", "content": "hack"})

# 写入结果文件
output = "\n".join(results)
with open("/tmp/auth_verify_result.txt", "w") as f:
    f.write(output)
print(output)
