import paramiko
import os
import sys
from dotenv import load_dotenv

# 加载 .env.local 中的环境变量
load_dotenv('.env.local')

SERVER_IP = os.getenv('DEPLOY_SERVER_IP')
SSH_PORT = int(os.getenv('DEPLOY_SSH_PORT', 22))
SSH_USER = os.getenv('DEPLOY_SSH_USER')
SSH_PASSWORD = os.getenv('DEPLOY_SSH_PASSWORD')
REMOTE_DIR = os.getenv('DEPLOY_REMOTE_DIR')

if not all([SERVER_IP, SSH_USER, SSH_PASSWORD, REMOTE_DIR]):
    print("Error: Missing deployment configuration in .env.local")
    sys.exit(1)

def deploy_fix():
    print("--- 准备通过 paramiko 部署 aixin/server/src/core/identity.js 并重启 aixin_server ---")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # 1. 连接服务器
        print(f"Connecting to {SERVER_IP}:{SSH_PORT} as {SSH_USER}...")
        ssh.connect(SERVER_IP, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD)
        print("Connected successfully!")
        
        # 2. 上传文件
        local_file = 'aixin/server/src/core/identity.js'
        remote_file = f"{REMOTE_DIR}/server/src/core/identity.js"
        
        print(f"Uploading {local_file} to {remote_file}...")
        sftp = ssh.open_sftp()
        sftp.put(local_file, remote_file)
        print("Upload successful!")
        sftp.close()
        
        # 3. 重启服务器服务
        print("Restarting aixin_server with pm2...")
        stdin, stdout, stderr = ssh.exec_command("pm2 restart aixin_server")
        exit_status = stdout.channel.recv_exit_status()
        
        if exit_status == 0:
            print("Server restarted successfully!")
            print(stdout.read().decode('utf-8'))
        else:
            print("Error restarting server:")
            print(stderr.read().decode('utf-8'))
            
    except Exception as e:
        print(f"Deployment failed: {e}")
    finally:
        ssh.close()
        print("SSH connection closed.")

if __name__ == '__main__':
    deploy_fix()
