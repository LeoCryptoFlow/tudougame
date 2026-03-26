# -*- coding: utf-8 -*-
"""修复 better-sqlite3 版本不兼容问题并确保服务正常运行"""
import os, paramiko

host = "43.135.138.144"
passwd = os.environ.get("AIXIN_PASS")
if not passwd: raise RuntimeError("设置 AIXIN_PASS")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username="root", password=passwd, timeout=15)

def run(cmd, desc=""):
    _, o, e = ssh.exec_command(cmd)
    o.channel.recv_exit_status()
    out = o.read().decode().strip()
    err = e.read().decode().strip()
    print(f"\n[{desc}]")
    if out: print(f"  {out[:300]}")
    if err: print(f"  stderr: {err[:300]}")
    return out

# 1. npm rebuild better-sqlite3
run("cd /root/aixin/server && npm rebuild better-sqlite3 2>&1 | tail -5", "rebuild better-sqlite3")

# 2. 停旧进程
run("pkill -f 'node.*index' 2>&1; sleep 2; echo done", "停止旧进程")

# 3. 启动新进程
run("cd /root/aixin/server && nohup node src/index.js > /tmp/aixin.log 2>&1 & sleep 3 && tail -5 /tmp/aixin.log", "启动服务")

# 4. 验证
import time; time.sleep(2)
run("curl -s https://aixin.chat/api/auth/login -X POST -H 'Content-Type: application/json' -d '{\"axId\":\"test\",\"password\":\"wrong\"}' 2>/dev/null", "验证登录接口")
run("curl -s https://aixin.chat/api/messages/test/unread 2>/dev/null", "验证受保护接口")
run("curl -s -o /dev/null -w 'HTTP %{http_code}' https://aixin.chat/api/agents 2>/dev/null", "验证公开接口")

ssh.close()
print("\n=== 完成 ===")
