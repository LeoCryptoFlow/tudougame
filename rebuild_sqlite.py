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
    
    # 因为报错说明了 module 是针对别版本的 node 编译的，我们需要回到旧版本的 node 或者 re-compile native modules 
    # 升级 better-sqlite3 以匹配新的 Node版本！
    cmd = """
    source ~/.nvm/nvm.sh
    cd /root/aixin/server
    echo "Installing latest better-sqlite3 (compatible with Node 22+)..."
    npm install better-sqlite3@11.1.2 sqlite3@latest
    pm2 restart index
    sleep 2
    pm2 logs index --lines 20 --nostream
    """

    stdin, stdout, stderr = ssh.exec_command(cmd)
    
    print("\n--- Command Output ---")
    for line in stdout:
        print(line, end="")

    print("\n--- Command Errors ---")
    for line in stderr:
        print(line, end="")

    ssh.close()
    
except Exception as e:
    print(f"❌ 发生错误: {e}")
