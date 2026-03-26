#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""最终验证：邮箱验证码 + 限频功能"""
import paramiko
import json

HOST = '43.135.138.144'
USER = 'root'
PASS = 'Quan1983@204'
PORT = 3210

def run(ssh, cmd, timeout=30):
    _, o, e = ssh.exec_command(cmd, timeout=timeout)
    o.channel.recv_exit_status()
    return o.read().decode('utf-8', errors='replace').strip()

def curl_post(ssh, path, data):
    body = json.dumps(data).replace('"', '\\"')
    cmd = f'curl -s -X POST http://localhost:{PORT}{path} -H "Content-Type: application/json" -d "{body}"'
    return run(ssh, cmd)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASS, timeout=15)

print('=' * 50)
print('爱信注册 邮箱验证码+防刷 最终验证')
print('=' * 50)

# 1. 发送验证码
print('\n[1] 发送验证码...')
r = curl_post(ssh, '/api/auth/send-code', {'email': 'yuntest@qq.com'})
print('结果:', r)
try:
    data = json.loads(r)
    dev_code = data.get('dev_code', '')
    print(f'验证码: {dev_code}')
except:
    dev_code = ''
    print('解析失败')

# 2. 重复发送（1分钟冷却）
print('\n[2] 重复发送（应被冷却限制）...')
r = curl_post(ssh, '/api/auth/send-code', {'email': 'yuntest@qq.com'})
print('结果:', r)

# 3. 无验证码注册（应被拒绝）
print('\n[3] 无验证码注册（应拒绝）...')
r = curl_post(ssh, '/api/agents', {
    'nickname': '测试用户',
    'email': 'yuntest@qq.com',
    'emailCode': ''
})
print('结果:', r)

# 4. 错误验证码注册（应被拒绝）
print('\n[4] 错误验证码注册（应拒绝）...')
r = curl_post(ssh, '/api/agents', {
    'nickname': '测试用户',
    'email': 'yuntest@qq.com',
    'emailCode': '000000'
})
print('结果:', r)

# 5. 正确验证码注册（应成功）
if dev_code:
    print(f'\n[5] 正确验证码 {dev_code} 注册（应成功）...')
    r = curl_post(ssh, '/api/agents', {
        'nickname': '测试用户',
        'email': 'yuntest@qq.com',
        'emailCode': dev_code
    })
    print('结果:', r)

# 6. 限频测试（快速请求）
print('\n[6] 限频测试（快速多次请求）...')
for i in range(6):
    r = curl_post(ssh, '/api/auth/send-code', {'email': f'limit{i}@test.com'})
    try:
        d = json.loads(r)
        status = 'OK' if d.get('ok') else f'拒绝: {d.get("error","")}'
    except:
        status = r[:60]
    print(f'  第{i+1}次: {status}')

print('\n' + '=' * 50)
print('验证完成！')
print("""
接口说明：
  POST /api/auth/send-code  {"email":"xxx"}  → 发送验证码
  POST /api/agents  {"nickname","email","emailCode"}  → 注册

防刷规则：
  send-code: 每IP每小时5次，同邮箱1分钟冷却
  注册接口: 每IP每10分钟5次
""")

ssh.close()
