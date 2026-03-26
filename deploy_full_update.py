# -*- coding: utf-8 -*-
import paramiko
import os

host = "43.135.138.144"
user = "root"
passwd = "Quan1983@204"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=passwd, timeout=15)

print("=== 更新爱信服务器 ===\n")

# 1. 上传最新的后端代码文件
print("1. 上传后端核心文件...")
sftp = ssh.open_sftp()

files_to_upload = [
    ("aixin/server/src/api/routes.js", "/root/aixin/server/src/api/routes.js"),
    ("aixin/server/src/core/identity.js", "/root/aixin/server/src/core/identity.js"),
    ("aixin/server/src/database/db.js", "/root/aixin/server/src/database/db.js"),
    ("aixin/website/index.html", "/root/aixin/website/index.html"),
]

for local, remote in files_to_upload:
    local_path = f"/Users/yunmishu/shengcode/{local}"
    if os.path.exists(local_path):
        try:
            sftp.put(local_path, remote)
            print(f"  ✅ {local}")
        except Exception as e:
            print(f"  ⚠️  上传失败 {local}: {e}")
    else:
        print(f"  ⚠️  跳过 {local} (本地不存在)")

sftp.close()

# 2. 重启 Node.js 进程
print("\n2. 重启后端服务...")
i, o, e = ssh.exec_command("kill -9 1165588 && cd /root/aixin/server && nohup node src/index.js > /dev/null 2>&1 & echo $!")
o.channel.recv_exit_status()
new_pid = o.read().decode().strip()
print(f"  ✅ 新进程 PID: {new_pid}")

# 3. 等待服务启动
print("\n3. 等待服务启动...")
import time
time.sleep(3)

# 4. 验证服务
print("\n4. 验证服务状态...")
i, o, e = ssh.exec_command("ps aux | grep 'node.*index.js' | grep -v grep")
o.channel.recv_exit_status()
result = o.read().decode().strip()
if result:
    print(f"  ✅ 服务运行中:\n  {result}")
else:
    print("  ⚠️  服务可能未启动")

# 5. 测试 API
print("\n5. 测试 API...")
i, o, e = ssh.exec_command("curl -s http://localhost:3000/api/agents | head -c 100")
o.channel.recv_exit_status()
api_result = o.read().decode().strip()
if api_result:
    print(f"  ✅ API 响应: {api_result}...")
else:
    print("  ⚠️  API 无响应")

ssh.close()
print("\n✅ 更新完成！")
