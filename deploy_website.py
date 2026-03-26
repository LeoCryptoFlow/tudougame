import paramiko, sys

HOST = '43.135.138.144'
USER = 'root'
PASS = 'Quan1983@204'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASS, timeout=15)
sftp = ssh.open_sftp()

local = '/Users/yunmishu/shengcode/aixin/website/index.html'
remote = '/root/aixin/website/index.html'

sftp.put(local, remote)
print('✅ index.html 上传成功')

sftp.close()
ssh.close()
print('🎉 部署完成！')
