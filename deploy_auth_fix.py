# -*- coding: utf-8 -*-
"""
安全修复部署脚本 — 修复「仅凭号码无需密码即可登录」漏洞
1. 上传 auth.js（JWT 认证模块）和 routes.js（加了认证保护的路由）
2. 在服务器安装 jsonwebtoken 依赖
3. 重启 Node.js 服务
4. 验证修复效果
"""
import os
import time
import paramiko

host   = os.environ.get("AIXIN_HOST", "43.135.138.144")
user   = os.environ.get("AIXIN_USER", "root")
passwd = os.environ.get("AIXIN_PASS")

if not passwd:
    raise RuntimeError("请设置环境变量 AIXIN_PASS，例如：export AIXIN_PASS='your_password'")

# 本地 -> 远程 文件映射
FILES = [
    ("aixin/server/src/utils/auth.js",   "/root/aixin/server/src/utils/auth.js"),
    ("aixin/server/src/api/routes.js",    "/root/aixin/server/src/api/routes.js"),
]

BASE_DIR = "/Users/yunmishu/shengcode"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
print(f"连接 {host} ...")
ssh.connect(host, username=user, password=passwd, timeout=15)

def run(cmd, desc=""):
    """执行远程命令并返回输出"""
    _, o, e = ssh.exec_command(cmd)
    o.channel.recv_exit_status()
    out = o.read().decode().strip()
    err = e.read().decode().strip()
    label = desc or cmd[:60]
    if err and "error" in err.lower():
        print(f"  ⚠️  {label}: {err}")
    else:
        print(f"  ✅ {label}: {out or 'ok'}")
    return out

# 1. 确保远程目录存在
run("mkdir -p /root/aixin/server/src/utils", "确保 utils 目录存在")

# 2. 上传文件
sftp = ssh.open_sftp()
for local_rel, remote in FILES:
    local_abs = os.path.join(BASE_DIR, local_rel)
    if not os.path.exists(local_abs):
        print(f"  跳过（不存在）: {local_rel}")
        continue
    try:
        sftp.put(local_abs, remote)
        print(f"  ✅ 上传: {local_rel} → {remote}")
    except Exception as e:
        print(f"  ❌ 失败: {local_rel} — {e}")
sftp.close()

# 3. 安装 jsonwebtoken 依赖
print("\n安装 jsonwebtoken 依赖...")
run("cd /root/aixin/server && npm install jsonwebtoken --save 2>&1 | tail -3", "npm install jsonwebtoken")

# 4. 重启 Node.js 后端
print("\n重启服务...")
run(
    "NODE_PID=$(pgrep -f 'node.*index.js' | head -1); "
    "[ -n \"$NODE_PID\" ] && kill $NODE_PID && sleep 1; "
    "cd /root/aixin/server && nohup node src/index.js > /tmp/aixin.log 2>&1 & "
    "echo node_pid_$!",
    "重启 Node.js backend"
)

# 5. 等待服务启动
print("\n等待服务启动 (3s)...")
time.sleep(3)

# 6. 验证修复：无 token 访问受保护接口应返回 401
print("\n验证安全修复...")
run(
    "curl -s -w '\\nHTTP_CODE:%{http_code}' "
    "https://aixin.chat/api/messages/test-user/unread 2>/dev/null",
    "无 token 访问受保护接口 → 应返回 401"
)

# 7. 验证登录接口可用
run(
    "curl -s -X POST https://aixin.chat/api/auth/login "
    "-H 'Content-Type: application/json' "
    "-d '{\"axId\":\"test\",\"password\":\"wrong\"}' 2>/dev/null",
    "登录接口测试（错误密码 → 应返回错误）"
)

# 8. 验证公开接口仍然正常
run(
    "curl -s -o /dev/null -w 'HTTP %{http_code}' "
    "https://aixin.chat/api/agents 2>/dev/null",
    "公开接口 /api/agents → 应返回 200"
)

# 9. 检查启动日志有无错误
run("tail -5 /tmp/aixin.log", "最近服务日志")

ssh.close()
print("\n✅ 安全修复部署完成！")
print("\n修复摘要：")
print("  • 新增 /api/auth/login 登录接口（AI-ID + 密码 → JWT Token）")
print("  • 注册成功后自动返回 token")
print("  • 所有敏感 API 添加 authMiddleware 认证保护：")
print("    - PUT /agents/:axId（修改资料）")
print("    - POST /contacts/*（好友操作）")
print("    - POST/GET /messages/*（收发消息）")
print("    - POST /groups/*（群组操作）")
print("    - POST /tasks（任务委派）")
print("    - POST/DELETE/GET /blacklist（黑名单）")
print("    - POST/GET /auto-accept（自动通过规则）")
print("    - POST /moments（发布动态）")
print("  • 每个受保护接口都验证 token 中的用户身份，防止冒充他人操作")
print("  • 公开接口（查看 Agent、搜索、技能市场）不受影响")
