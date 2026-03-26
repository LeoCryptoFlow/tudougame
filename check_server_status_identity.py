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
    
    # 使用正确的 npm 路径查找日志
    stdin, stdout, stderr = ssh.exec_command("source ~/.nvm/nvm.sh && pm2 logs index --lines 50 --nostream")
    print("\n--- PM2 Logs (index) ---")
    print(stdout.read().decode())
    print(stderr.read().decode())
    
    stdin, stdout, stderr = ssh.exec_command("source ~/.nvm/nvm.sh && pm2 logs aixin-server --lines 10 --nostream")
    print("\n--- PM2 Logs (aixin-server) ---")
    print(stdout.read().decode())

    stdin, stdout, stderr = ssh.exec_command("source ~/.nvm/nvm.sh && pm2 status")
    print("\n--- PM2 Status ---")
    print(stdout.read().decode())

    ssh.close()
    
except Exception as e:
    print(f"❌ 发生错误: {e}")
