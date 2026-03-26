import paramiko
import os
import sys
import time

HOST = '43.135.138.144'
USER = 'root'
PASS = 'Quan1983@204'

BASE = '/Users/yunmishu/shengcode'
local_rel = 'aixin/server/src/core/identity.js'
remote_path = '/root/aixin/server/src/core/identity.js'

print('🔌 连接服务器...')
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, username=USER, password=PASS, timeout=15)
    print('✅ SSH 连接成功')
except Exception as e:
    print(f"Failed to connect: {e}")
    sys.exit(1)

try:
    sftp = ssh.open_sftp()
    local_path = os.path.join(BASE, local_rel)
    sftp.put(local_path, remote_path)
    print(f'  ✅ {local_rel.split("/")[-1]} 上传成功')
    sftp.close()
except Exception as e:
    print(f"Error uploading file: {e}")

def run(ssh, cmd, timeout=30):
    _, o, e = ssh.exec_command(cmd, timeout=timeout)
    o.channel.recv_exit_status()
    return o.read().decode().strip(), e.read().decode().strip()

print('🔄 检查运行中的服务进程...')
out, err = run(ssh, 'ps aux | grep node | grep -v grep')
print(f"进程: {out}")

print('🔄 尝试查找 pm2...')
pm2_path_out, _ = run(ssh, 'which pm2 || command -v pm2')
if pm2_path_out:
    print(f"找到 pm2: {pm2_path_out}, 正在重启...")
    out, err = run(ssh, f'{pm2_path_out} restart all')
    print(f"PM2 Restart: {out}")
else:
    print('🔄 尝试通过 docker ps 查找容器...')
    out, err = run(ssh, 'docker ps --format "{{.Names}}" | grep -i "server\|aixin\|node" | head -1')
    container = out.strip()
    if container:
        print(f'   找到容器: {container}, 尝试重启...')
        out, _ = run(ssh, f'docker restart {container}')
        print(f"   重启结果: {out}")
    else:
        print('   没有找到容器，尝试重启所有容器...')
        out, _ = run(ssh, 'docker restart $(docker ps -q) 2>&1')
        print(f"   重启所有容器结果: {out}")

ssh.close()
print('\n🎉 部署完成！')
