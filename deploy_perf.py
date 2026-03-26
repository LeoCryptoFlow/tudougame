# -*- coding: utf-8 -*-
"""
性能优化部署脚本
上传修改的服务器文件并重启
"""
import os
import paramiko

host   = os.environ.get("AIXIN_HOST", "43.135.138.144")
user   = os.environ.get("AIXIN_USER", "root")
passwd = os.environ.get("AIXIN_PASS")

if not passwd:
    raise RuntimeError("请设置环境变量 AIXIN_PASS，例如：export AIXIN_PASS='your_password'")

# 本地 -> 远程 文件映射
FILES = [
    ("aixin/server/src/database/db.js",    "/root/aixin/server/src/database/db.js"),
    ("aixin/server/src/core/identity.js",  "/root/aixin/server/src/core/identity.js"),
    ("aixin/server/src/api/routes.js",     "/root/aixin/server/src/api/routes.js"),
    ("aixin/server/src/index.js",          "/root/aixin/server/src/index.js"),
    ("aixin/deploy/nginx.conf",            "/etc/nginx/conf.d/aixin.conf"),
]

BASE_DIR = "/Users/yunmishu/shengcode"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
print(f"连接 {host} ...")
ssh.connect(host, username=user, password=passwd, timeout=15)

# 1. 上传所有修改的文件
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

print("\n重启服务...")

# 2. 测试 nginx 配置
run("nginx -t 2>&1", "nginx 配置测试")

# 3. 重启 Node.js 后端（直接 kill + nohup 重启）
run(
    "NODE_PID=$(pgrep -f 'node.*index.js' | head -1); "
    "[ -n \"$NODE_PID\" ] && kill $NODE_PID && sleep 1; "
    "cd /root/aixin/server && nohup node src/index.js > /tmp/aixin.log 2>&1 & "
    "echo node_pid_$!",
    "重启 Node.js backend"
)

# 4. Reload nginx（不中断连接）
run("nginx -s reload 2>&1 || true", "nginx reload")

# 5. 等待服务恢复
import time
print("\n等待服务启动 (3s)...")
time.sleep(3)

# 6. 验证：测试 API 响应时间
run(
    "curl -s -o /dev/null -w 'HTTP %{http_code}  TTFB: %{time_starttransfer}s  Total: %{time_total}s' "
    "https://aixin.chat/api/agents 2>/dev/null",
    "API 响应时间测试"
)

run(
    "curl -s -o /dev/null -w 'HTTP %{http_code}  TTFB: %{time_starttransfer}s' "
    "https://aixin.chat/health 2>/dev/null",
    "健康检查"
)

ssh.close()
print("\n✅ 部署完成！")
print("\n性能优化摘要：")
print("  • SQLite: synchronous=NORMAL（比FULL快5-10x）")
print("  • SQLite: 32MB cache + 256MB mmap（减少磁盘I/O）")
print("  • 新增6个复合索引（未读消息、聊天记录、好友状态）")
print("  • GET /agents 添加分页（默认limit=50）")
print("  • /portal/stats 增加10秒内存缓存")
print("  • /skill/install 去掉每次请求的CREATE TABLE")
print("  • WebSocket presence 改为定向好友推送（O(1)替代O(n)广播）")
print("  • nginx keepalive连接池 32条 + 缓冲区8k→16k")
print("  • nginx /api/agents 允许5秒公开缓存")
