import paramiko

HOST = '43.135.138.144'
USER = 'root'
PASS = 'Quan1983@204'

print('🔌 连接服务器...')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASS, timeout=15)
print('✅ SSH 连接成功')

sftp = ssh.open_sftp()

# 上传 routes.js
sftp.put('aixin/server/src/api/routes.js', '/root/aixin/server/src/api/routes.js')
print('✅ routes.js 上传成功')

# 上传 auth.js
sftp.put('aixin/server/src/utils/auth.js', '/root/aixin/server/src/utils/auth.js')
print('✅ auth.js 上传成功')

# 验证 hint 字段存在
stdin, stdout, stderr = ssh.exec_command('grep -c "hint" /root/aixin/server/src/api/routes.js')
print(f'routes.js 中 hint 出现次数: {stdout.read().decode().strip()}')

stdin, stdout, stderr = ssh.exec_command('grep -c "hint" /root/aixin/server/src/utils/auth.js')
print(f'auth.js 中 hint 出现次数: {stdout.read().decode().strip()}')

# 重启服务
stdin, stdout, stderr = ssh.exec_command('pm2 restart aixin-server --update-env 2>&1')
print(stdout.read().decode())

# 等待并检查状态
import time
time.sleep(3)
stdin, stdout, stderr = ssh.exec_command('pm2 status 2>&1')
print(stdout.read().decode())

sftp.close()
ssh.close()
print('🎉 部署完成！')
