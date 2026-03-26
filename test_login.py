# -*- coding: utf-8 -*-
"""测试登录接口"""
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
    if out: print(f"  {out[:500]}")
    if err: print(f"  stderr: {err[:300]}")
    return out

# 1. 检查服务是否正在运行
run("pgrep -af 'node.*index' | head -3", "Node 进程")

# 2. 直接通过 localhost 测试登录（跳过 nginx）
run(
    "curl -s -X POST http://localhost:3210/api/auth/login "
    "-H 'Content-Type: application/json' "
    "-d '{\"axId\":\"AI-751891\",\"password\":\"123123\"}'",
    "本地测试登录 AI-751891"
)

# 3. 通过 https 域名测试
run(
    "curl -s -X POST https://aixin.chat/api/auth/login "
    "-H 'Content-Type: application/json' "
    "-d '{\"axId\":\"AI-751891\",\"password\":\"123123\"}'",
    "HTTPS 测试登录 AI-751891"
)

# 4. 检查数据库中该用户的密码字段
run(
    "cd /root/aixin/server && node -e \""
    "const {getDb}=require('./src/database/db');"
    "const db=getDb();"
    "const a=db.prepare('SELECT ax_id,password,nickname FROM agents WHERE ax_id=?').get('AI-751891');"
    "console.log(JSON.stringify(a));\"",
    "数据库中 AI-751891 的密码"
)

# 5. 检查 routes.js 中的 auth/login 路由是否在
run("grep -A5 'auth/login' /root/aixin/server/src/api/routes.js | head -10", "routes.js 中的 login 路由")

# 6. 查看最近日志
run("tail -20 /tmp/aixin.log 2>/dev/null", "最近服务日志")

ssh.close()
print("\n=== 完成 ===")
