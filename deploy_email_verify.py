#!/usr/bin/env python3
"""
部署邮箱验证码 + 接口限频功能到服务器
"""
import subprocess
import sys

SERVER = "root@aixin.chat"
REMOTE_DIR = "/opt/aixin/server"

FILES = [
    ("aixin/server/src/api/routes.js",         f"{REMOTE_DIR}/src/api/routes.js"),
    ("aixin/server/src/core/identity.js",       f"{REMOTE_DIR}/src/core/identity.js"),
    ("aixin/server/src/database/db.js",         f"{REMOTE_DIR}/src/database/db.js"),
    ("aixin/server/src/utils/rateLimit.js",     f"{REMOTE_DIR}/src/utils/rateLimit.js"),
    ("aixin/server/src/utils/emailVerify.js",   f"{REMOTE_DIR}/src/utils/emailVerify.js"),
]

def run(cmd, check=True):
    print(f"  $ {cmd}")
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.stdout.strip():
        print(r.stdout)
    if r.stderr.strip():
        print(r.stderr, file=sys.stderr)
    if check and r.returncode != 0:
        print(f"❌ 命令失败: {cmd}")
        sys.exit(1)
    return r

print("🚀 开始部署邮箱验证 + 限频功能...")

# 1. 创建远程目录
print("\n📁 创建远程 utils 目录...")
run(f'ssh {SERVER} "mkdir -p {REMOTE_DIR}/src/utils"')

# 2. 上传文件
print("\n📤 上传文件...")
for local, remote in FILES:
    print(f"  上传 {local} → {remote}")
    run(f"scp {local} {SERVER}:{remote}")

# 3. 重启服务
print("\n🔄 重启 PM2 服务...")
run(f'ssh {SERVER} "cd {REMOTE_DIR} && pm2 restart aixin-server 2>/dev/null || pm2 start src/index.js --name aixin-server"')

# 4. 等待启动
import time
time.sleep(2)

# 5. 检查服务状态
print("\n✅ 检查服务状态...")
r = run(f'ssh {SERVER} "pm2 list | grep aixin"', check=False)

# 6. 验证接口
print("\n🧪 验证接口可用性...")
r = run(f'ssh {SERVER} "curl -s -o /dev/null -w \'%{{http_code}}\' http://localhost:3000/api/portal/stats"', check=False)
if '200' in r.stdout:
    print("✅ 服务正常响应")
else:
    print(f"⚠️  响应码: {r.stdout}")

print("""
🎉 部署完成！

新增功能：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📧 邮箱验证码注册
  POST /api/auth/send-code   发送验证码
  POST /api/agents           注册（带 email + emailCode）

🛡️  接口防刷限频
  发送验证码：每IP每小时最多5次，超限封禁30分钟
  注册接口：  每IP每10分钟最多5次，超限封禁1小时
  响应头：    X-RateLimit-Limit / Remaining / Reset

🗄️  数据库升级
  agents 表新增 email、email_verified 字段
  自动迁移存量数据，无需手动操作
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

注册流程：
  1. POST /api/auth/send-code  { "email": "xxx@qq.com" }
  2. POST /api/agents  { "nickname": "...", "email": "xxx@qq.com", "emailCode": "123456" }
""")

if __name__ == "__main__":
    pass
