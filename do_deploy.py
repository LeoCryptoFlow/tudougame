#!/usr/bin/env python3
"""通过 paramiko SSH 部署爱信邮箱验证+限频功能"""
import paramiko
import os
import time

HOST = '43.135.138.144'
USER = 'root'
PASS = 'Quan1983@204'

FILES = [
    ('aixin/server/src/api/routes.js',        '/root/aixin/server/src/api/routes.js'),
    ('aixin/server/src/core/identity.js',     '/root/aixin/server/src/core/identity.js'),
    ('aixin/server/src/database/db.js',       '/root/aixin/server/src/database/db.js'),
    ('aixin/server/src/utils/rateLimit.js',   '/root/aixin/server/src/utils/rateLimit.js'),
    ('aixin/server/src/utils/emailVerify.js', '/root/aixin/server/src/utils/emailVerify.js'),
]

BASE = '/Users/yunmishu/shengcode'

def run(ssh, cmd, timeout=30):
    _, o, e = ssh.exec_command(cmd, timeout=timeout)
    o.channel.recv_exit_status()
    return o.read().decode().strip(), e.read().decode().strip()

print('🔌 连接服务器...')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASS, timeout=15)
print('✅ SSH 连接成功')

# 1. 创建 utils 目录
run(ssh, 'mkdir -p /root/aixin/server/src/utils')
print('📁 utils 目录已创建')

# 2. 上传文件
sftp = ssh.open_sftp()
for local_rel, remote_path in FILES:
    local_path = os.path.join(BASE, local_rel)
    sftp.put(local_path, remote_path)
    print(f'  ✅ {local_rel.split("/")[-1]}')
sftp.close()

# 3. 查看 docker 容器
out, _ = run(ssh, 'docker ps --format "{{.Names}}\t{{.Ports}}"')
print(f'\n📦 运行中的容器:\n{out}')

# 4. 重启服务容器（找含 server 或 aixin 的容器）
out, _ = run(ssh, 'docker ps --format "{{.Names}}" | grep -i "server\|aixin\|node" | head -1')
container = out.strip()
if container:
    print(f'\n🔄 重启容器: {container}')
    out, _ = run(ssh, f'docker restart {container}')
    print(out)
else:
    # 重启所有容器
    print('\n🔄 重启所有容器...')
    out, _ = run(ssh, 'docker restart $(docker ps -q) 2>&1')
    print(out)

print('⏳ 等待服务启动...')
time.sleep(4)

# 5. 检测哪个端口可用
active_port = None
for port in [3000, 3210, 8080, 80]:
    out, _ = run(ssh, f'curl -s -o /dev/null -w "%{{http_code}}" http://localhost:{port}/api/portal/stats')
    if out == '200':
        active_port = port
        print(f'✅ 服务运行在端口 {port}')
        break
    else:
        print(f'   port {port}: {out or "no response"}')

if active_port:
    # 6. 测试新接口
    out, _ = run(ssh, f'curl -s -X POST http://localhost:{active_port}/api/auth/send-code -H "Content-Type: application/json" -d \'{{"email":"test@qq.com"}}\'')
    print(f'\n📧 测试 send-code 接口: {out}')

    out, _ = run(ssh, f'curl -s -X POST http://localhost:{active_port}/api/agents -H "Content-Type: application/json" -d \'{{"nickname":"测试","email":"no-code@qq.com","emailCode":""}}\'')
    print(f'📝 测试无验证码注册(应拒绝): {out}')
else:
    print('\n⚠️  未检测到服务，请手动检查')
    out, _ = run(ssh, 'docker ps && netstat -tlnp 2>/dev/null | grep node')
    print(out)

ssh.close()
print('\n🎉 部署完成！')
print("""
新增功能说明：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📧 邮箱验证码注册流程：
  1. POST /api/auth/send-code  {"email":"xxx@qq.com"}
     → 发送验证码（1分钟冷却，每IP每小时最多5次）
  2. POST /api/agents  {"nickname":"...", "email":"xxx@qq.com", "emailCode":"123456"}
     → 注册成功（邮箱唯一，验证码5分钟有效，最多错误5次）

🛡️ 接口防刷：
  - send-code：每IP每小时5次，超限封禁30分钟
  - 注册接口：每IP每10分钟5次，超限封禁1小时
  - 响应头：X-RateLimit-Limit / Remaining / Reset

🗄️ 数据库：agents表自动迁移增加 email/email_verified 字段
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
