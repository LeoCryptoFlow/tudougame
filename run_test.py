#!/usr/bin/env python3
import paramiko, time, json

HOST = '43.135.138.144'
USER = 'root'
PASS = 'Quan1983@204'

results = {}
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASS, timeout=15)

# 测试密码校验（服务端本地 curl，绕过 IP 限流）
tests = [
    ('无密码_应拒绝',    '{"nickname":"T1","agent_type":"personal"}'),
    ('短密码_应拒绝',    '{"nickname":"T2","agent_type":"personal","password":"123"}'),
    ('合格密码_应成功',  '{"nickname":"T3ok","agent_type":"personal","password":"abc123xyz"}'),
    ('bot无密码_应成功', '{"nickname":"Bot99","agent_type":"bot"}'),
    ('skill无密码_应成功','{"nickname":"Skill99","agent_type":"skill"}'),
]
for name, payload in tests:
    cmd = f"curl -s -X POST http://localhost:3210/api/agents -H 'Content-Type: application/json' -d '{payload}'"
    _, o, _ = ssh.exec_command(cmd)
    r = o.read().decode()
    results[name] = json.loads(r) if r else 'empty'
    time.sleep(0.3)

ssh.close()

out_path = '/Users/yunmishu/shengcode/final_test_output.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(json.dumps(results, ensure_ascii=False, indent=2))
