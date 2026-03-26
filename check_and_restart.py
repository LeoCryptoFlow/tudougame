#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import paramiko
import time

HOST = '43.135.138.144'
USER = 'root'
PASS = 'Quan1983@204'

def run(ssh, cmd, timeout=30):
    _, o, e = ssh.exec_command(cmd, timeout=timeout)
    o.channel.recv_exit_status()
    return o.read().decode('utf-8', errors='replace').strip()

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASS, timeout=15)
print('SSH OK')

# 查看当前状态
print('=== Node 进程 ===')
print(run(ssh, 'ps aux | grep node | grep -v grep | head -5'))

print('=== 端口 3210 ===')
print(run(ssh, 'ss -tlnp | grep 3210 || echo "未监听"'))

print('=== 服务日志 ===')
print(run(ssh, 'tail -15 /tmp/aixin.log 2>/dev/null || echo "无日志"'))

# 测试接口
code = run(ssh, 'curl -s -o /dev/null -w "%{http_code}" http://localhost:3210/api/portal/stats')
print(f'\n=== 接口状态: {code} ===')

if code == '200':
    r = run(ssh, 'curl -s -X POST http://localhost:3210/api/auth/send-code -H "Content-Type: application/json" -d \'{"email":"test@qq.com"}\'')
    print('send-code:', r)
else:
    print('服务未响应，重新启动...')
    # 清理
    run(ssh, 'pkill -9 -f node 2>/dev/null || true')
    run(ssh, 'fuser -k 3210/tcp 2>/dev/null || true')
    time.sleep(2)
    # 启动
    run(ssh, 'cd /root/aixin/server && nohup node src/index.js > /tmp/aixin.log 2>&1 &')
    time.sleep(5)
    # 再次检查
    code2 = run(ssh, 'curl -s -o /dev/null -w "%{http_code}" http://localhost:3210/api/portal/stats')
    print('重启后:', code2)
    print(run(ssh, 'tail -10 /tmp/aixin.log'))

ssh.close()
print('Done')
