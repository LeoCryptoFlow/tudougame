# -*- coding: utf-8 -*-
"""最终修复：清理旧进程 + 确保登录正常"""
import os, time, paramiko

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
    if out: print(f"  {out[:500]}")
    if err: print(f"  stderr: {err[:300]}")
    return out

# 1. 杀掉所有旧的 Node 进程
run("pkill -9 -f 'node.*index' 2>&1; sleep 2; echo 'all killed'", "杀掉所有旧进程")
run("pgrep -af 'node.*index' || echo '已全部停止'", "确认无残留")

# 2. 启动新进程
run("cd /root/aixin/server && nohup node src/index.js > /tmp/aixin.log 2>&1 & sleep 3 && tail -5 /tmp/aixin.log", "启动新服务")

# 3. 确认只有一个进程
run("pgrep -af 'node.*index'", "当前 Node 进程")

# 4. 全面验证
time.sleep(2)

# 4a. 登录测试
run(
    "curl -s -X POST https://aixin.chat/api/auth/login "
    "-H 'Content-Type: application/json' "
    "-d '{\"axId\":\"AI-751891\",\"password\":\"123123\"}'",
    "HTTPS 登录 AI-751891"
)

# 4b. 无 token 访问受保护接口
run("curl -s https://aixin.chat/api/messages/AI-751891/unread", "无token查未读（应401）")

# 4c. 用 token 访问受保护接口
login_resp = run(
    "curl -s -X POST http://localhost:3210/api/auth/login "
    "-H 'Content-Type: application/json' "
    "-d '{\"axId\":\"AI-751891\",\"password\":\"123123\"}'",
    "获取 token"
)

# 提取 token 并测试
run(
    "TOKEN=$(curl -s -X POST http://localhost:3210/api/auth/login "
    "-H 'Content-Type: application/json' "
    "-d '{\"axId\":\"AI-751891\",\"password\":\"123123\"}' | "
    "python3 -c 'import sys,json; print(json.load(sys.stdin).get(\"token\",\"\"))') && "
    "curl -s http://localhost:3210/api/messages/AI-751891/unread "
    "-H \"Authorization: Bearer $TOKEN\"",
    "带token查未读消息"
)

# 4d. 公开接口
run("curl -s -o /dev/null -w 'HTTP %{http_code}' https://aixin.chat/api/agents", "公开接口")

ssh.close()
print("\n=== 修复完成 ===")
