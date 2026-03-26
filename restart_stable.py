# -*- coding: utf-8 -*-
"""稳定重启：使用 pm2 或 systemd 确保服务不会因 SSH 断开而终止"""
import os, time, paramiko

host = "43.135.138.144"
passwd = os.environ.get("AIXIN_PASS")
if not passwd: raise RuntimeError("设置 AIXIN_PASS")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username="root", password=passwd, timeout=30)

def run(cmd, desc="", timeout=60):
    _, o, e = ssh.exec_command(cmd, timeout=timeout)
    o.channel.recv_exit_status()
    out = o.read().decode('utf-8', errors='replace').strip()
    err = e.read().decode('utf-8', errors='replace').strip()
    print(f"\n[{desc}]")
    if out: print(f"  {out[:600]}")
    if err: print(f"  stderr: {err[:300]}")
    return out

# 1. 检查当前状态
run("curl -s http://localhost:3210/api/agents 2>/dev/null | head -c 80", "当前服务状态")

# 2. 检查是否有 pm2
pm2 = run("which pm2 2>/dev/null || echo 'not found'", "检查 pm2")

if 'not found' in pm2:
    # 安装 pm2
    run("npm install -g pm2 2>&1 | tail -3", "安装 pm2")

# 3. 停掉所有旧进程
run("pkill -9 -f 'node.*index' 2>/dev/null; sleep 2; echo 'done'", "停旧进程")
run("pgrep -af 'node.*index' 2>/dev/null || echo 'clean'", "确认清理")

# 4. 用 pm2 启动（pm2 守护进程不依赖 SSH 会话）
run("cd /root/aixin/server && pm2 delete aixin 2>/dev/null; pm2 start src/index.js --name aixin 2>&1 | tail -10", "pm2 启动")

# 5. 等待启动
time.sleep(3)

# 6. 检查 pm2 状态
run("pm2 status 2>&1", "pm2 状态")

# 7. 检查日志
run("pm2 logs aixin --nostream --lines 10 2>&1", "pm2 日志")

# 8. 验证接口
run("curl -s http://localhost:3210/api/agents 2>/dev/null | head -c 80", "验证 /api/agents")

run(
    "curl -s -X POST http://localhost:3210/api/auth/login "
    "-H 'Content-Type: application/json' "
    "-d '{\"axId\":\"AI-751891\",\"password\":\"123123\"}' | head -c 100",
    "验证登录"
)

run("curl -s http://localhost:3210/api/messages/AI-751891/unread", "验证受保护（无token）")

# 9. 设置开机自启
run("pm2 save && pm2 startup 2>&1 | tail -3", "设置开机自启")

ssh.close()
print("\n=== 完成 ===")
