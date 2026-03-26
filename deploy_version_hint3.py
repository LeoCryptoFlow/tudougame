import paramiko
import time

HOST = '43.135.138.144'
USER = 'root'
PASS = 'Quan1983@204'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASS, timeout=15)

# 重启正确的进程名 aixin（不是 aixin-server）
stdin, stdout, stderr = ssh.exec_command('pm2 restart aixin 2>&1')
print('pm2 restart aixin:', stdout.read().decode().strip())
time.sleep(3)

# 测试
stdin, stdout, stderr = ssh.exec_command('curl -s -X POST http://localhost:3000/api/auth/login -H "Content-Type: application/json" -d \'{"username":"test","password":"123"}\'')
result = stdout.read().decode()
print(f'测试结果: {result}')

ssh.close()
