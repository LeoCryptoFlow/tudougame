# -*- coding: utf-8 -*-
"""
安全修复部署脚本 v2 — 修复部署问题
检查服务器上文件是否正确，排查启动失败原因
"""
import os
import time
import paramiko

host   = os.environ.get("AIXIN_HOST", "43.135.138.144")
user   = os.environ.get("AIXIN_USER", "root")
passwd = os.environ.get("AIXIN_PASS")

if not passwd:
    raise RuntimeError("请设置环境变量 AIXIN_PASS")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
print(f"连接 {host} ...")
ssh.connect(host, username=user, password=passwd, timeout=15)

def run(cmd, desc=""):
    _, o, e = ssh.exec_command(cmd)
    o.channel.recv_exit_status()
    out = o.read().decode().strip()
    err = e.read().decode().strip()
    label = desc or cmd[:80]
    print(f"\n  [{label}]")
    if out: print(f"  stdout: {out[:500]}")
    if err: print(f"  stderr: {err[:500]}")
    return out

# 1. 查看当前运行的 Node 进程
run("ps aux | grep 'node.*index' | grep -v grep", "当前 Node 进程")

# 2. 检查文件是否存在
run("ls -la /root/aixin/server/src/utils/auth.js /root/aixin/server/src/api/routes.js", "检查文件")

# 3. 检查 routes.js 是否有 auth/login
run("grep -n 'auth/login' /root/aixin/server/src/api/routes.js | head -5", "routes.js 是否包含 auth/login")

# 4. 检查 auth.js 是否有 authMiddleware
run("grep -n 'authMiddleware' /root/aixin/server/src/utils/auth.js | head -5", "auth.js 是否包含 authMiddleware")

# 5. 检查 jsonwebtoken 是否安装
run("ls /root/aixin/server/node_modules/jsonwebtoken/index.js 2>&1", "jsonwebtoken 是否安装")

# 6. 检查 package.json 是否有 jsonwebtoken
run("grep jsonwebtoken /root/aixin/server/package.json", "package.json 中的 jsonwebtoken")

# 如果 jsonwebtoken 未安装，安装它
run("cd /root/aixin/server && npm install jsonwebtoken --save 2>&1 | tail -5", "安装 jsonwebtoken")

# 7. 完全停止所有旧的 Node 进程
run("pkill -f 'node.*index' 2>&1; sleep 2; echo 'killed'", "停止所有旧进程")

# 8. 验证确实停了
run("pgrep -f 'node.*index' 2>&1 || echo '已全部停止'", "确认进程停止")

# 9. 尝试在前台启动检查是否有错误（只运行2秒就终止来看启动日志）
run("cd /root/aixin/server && timeout 3 node src/index.js > /tmp/aixin_test_start.log 2>&1; cat /tmp/aixin_test_start.log", "测试启动（查看是否有错误）")

# 10. 正式后台启动
run(
    "cd /root/aixin/server && nohup node src/index.js > /tmp/aixin.log 2>&1 &; "
    "sleep 3 && cat /tmp/aixin.log | tail -10",
    "正式启动并查看日志"
)

# 11. 验证
time.sleep(3)
run(
    "curl -s https://aixin.chat/api/auth/login -X POST "
    "-H 'Content-Type: application/json' "
    "-d '{\"axId\":\"test\",\"password\":\"wrong\"}' 2>/dev/null",
    "测试 /api/auth/login"
)

run(
    "curl -s https://aixin.chat/api/messages/test/unread 2>/dev/null",
    "测试受保护接口（无token）"
)

run(
    "curl -s https://aixin.chat/api/agents 2>/dev/null | head -c 100",
    "测试公开接口"
)

ssh.close()
print("\n=== 完成 ===")
