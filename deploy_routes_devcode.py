import paramiko
import os
import sys
import time

HOST = '43.135.138.144'
USER = 'root'
PASS = 'Quan1983@204'

print('🔌 连接服务器...')
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, username=USER, password=PASS, timeout=15)
    print('✅ SSH 连接成功')
    
    sftp = ssh.open_sftp()
except Exception as e:
    print(f"Failed to connect: {e}")
    sys.exit(1)

local_path = '/Users/yunmishu/shengcode/aixin/server/src/api/routes.js'
remote_path = '/root/aixin/server/src/api/routes.js'

try:
    sftp.put(local_path, remote_path)
    print('  ✅ routes.js 上传成功')
except Exception as e:
    print(f"  ❌ 上传失败: {e}")

sftp.close()

# 重启尝试逻辑
def run_nowait(ssh, cmd):
    _, o, _ = ssh.exec_command(cmd)

print('🔄 正在重启 Node 进程...')
run_nowait(ssh, 'pkill node')
time.sleep(3)

print("启动命令执行...")
run_nowait(ssh, "nohup /usr/bin/env node /root/aixin/server/src/index.js > /tmp/aixin.log 2>&1 &")

time.sleep(3)

_, o, _ = ssh.exec_command('ps aux | grep node | grep -v grep')
out = o.read().decode().strip()
print(f"新进程: {out}")

ssh.close()
print('\n🎉 部署并重启完成！')
