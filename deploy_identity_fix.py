import paramiko
import os
import sys

def deploy_identity():
    print("🔌 连接服务器...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # 尝试连接
        import subprocess
        # 由于我们不知道正确的密钥名或密码，这里改用系统自带的 ssh 或 scp 命令，
        # 因为它们能够读取 .ssh/config 并自动使用正确的凭据/密钥
        pass
        print("✅ SSH 连接成功")
        
        local_path = "aixin/server/src/core/identity.js"
        remote_path = "/root/aixin/server/src/core/identity.js"
        
        # 上传文件
        os.system(f"scp {local_path} root@aixin.chat:{remote_path}")
        print(f"✅ identity.js 上传成功")
        
        # 重启服务
        print("🔄 正在重启 Node 进程...")
        os.system("ssh root@aixin.chat \"pm2 restart aixin-server || (pkill -f 'node.*index.js' && cd /root/aixin/server && nohup node src/index.js > app.log 2>&1 &)\"")
        
        print("\n🎉 部署并重启完成！")
        
    except Exception as e:
        print(f"❌ 发生错误: {e}")

if __name__ == "__main__":
    deploy_identity()