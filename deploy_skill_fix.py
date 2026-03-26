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

local_path = '/Users/yunmishu/shengcode/aixin/skill/aixin-skill.py'
remote_path = '/skill/aixin-skill.py' # 根据之前代码，下载目录是 /skill/aixin-skill.py 或项目内

try:
    # 检查目标文件夹是否存在
    stdin, stdout, stderr = ssh.exec_command('ls /skill')
    if 'No such file or directory' in stderr.read().decode():
        remote_path = '/root/skill/aixin-skill.py'
        
    sftp.put(local_path, remote_path)
    print(f'  ✅ aixin-skill.py 上传成功至 {remote_path}')
except Exception as e:
    print(f"  ❌ 第一路径上传失败: {e}")
    try:
        remote_path = '/root/aixin/skill/aixin-skill.py'
        sftp.put(local_path, remote_path)
        print(f'  ✅ aixin-skill.py 上传成功至 {remote_path}')
    except Exception as e2:
        print(f"  ❌ 第二路径上传失败: {e2}")

sftp.close()
ssh.close()
print('\n🎉 Skill部署完成！')
