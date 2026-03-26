import paramiko
import time

HOST = '43.135.138.144'
USER = 'root'
PASS = 'Quan1983@204'

print('🔌 连接服务器...')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASS, timeout=15)
print('✅ SSH 连接成功')

sftp = ssh.open_sftp()

# 上传文件
sftp.put('aixin/server/src/api/routes.js', '/root/aixin/server/src/api/routes.js')
print('✅ routes.js 上传成功')

sftp.put('aixin/server/src/utils/auth.js', '/root/aixin/server/src/utils/auth.js')
print('✅ auth.js 上传成功')
sftp.close()

# 验证 hint 在文件中
stdin, stdout, stderr = ssh.exec_command('grep "hint" /root/aixin/server/src/api/routes.js | head -3')
out = stdout.read().decode()
print(f'✅ routes.js hint 验证:\n{out}')

# 停止并重新启动（不用 restart，用 stop + start 更可靠）
stdin, stdout, stderr = ssh.exec_command('pm2 stop aixin-server 2>&1')
print('pm2 stop:', stdout.read().decode().strip())
time.sleep(2)

stdin, stdout, stderr = ssh.exec_command('pm2 start aixin-server 2>&1')
print('pm2 start:', stdout.read().decode().strip())
time.sleep(3)

# 检查状态
stdin, stdout, stderr = ssh.exec_command('pm2 status 2>&1')
print(stdout.read().decode())

# 本地测试
stdin, stdout, stderr = ssh.exec_command('curl -s -X POST http://localhost:3000/api/auth/login -H "Content-Type: application/json" -d \'{"username":"test","password":"123"}\'')
result = stdout.read().decode()
print(f'🧪 本地测试结果: {result}')

ssh.close()
print('\n🎉 完成！')
