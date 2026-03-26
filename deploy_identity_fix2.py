import paramiko
import os
import sys

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

local_path = 'aixin/server/src/core/identity.js'
remote_path = '/root/aixin/server/src/core/identity.js'

try:
    sftp.put(local_path, remote_path)
    print(f'  ✅ identity.js 上传成功至 {remote_path}')
    
    # 重启服务
    print("🔄 正在重启 Node 进程...")
    ssh.exec_command("pm2 restart aixin-server || (pkill -f 'node.*index.js' && cd /root/aixin/server && nohup node src/index.js > app.log 2>&1 &)")
    
    print('\n🎉 部署并重启完成！')
    
except Exception as e:
    print(f"  ❌ 发生错误: {e}")

finally:
    sftp.close()
    ssh.close()
