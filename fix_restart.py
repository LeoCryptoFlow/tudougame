#!/usr/bin/env python3
import paramiko, time

HOST = '43.135.138.144'
USER = 'root'
PASS = 'Quan1983@204'

def run(ssh, cmd, timeout=60):
    _, o, e = ssh.exec_command(cmd, timeout=timeout)
    o.channel.recv_exit_status()
    return o.read().decode().strip(), e.read().decode().strip()

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASS, timeout=15)
print('✅ SSH 连接成功')

# 彻底 kill 占用 3210 端口的进程 + 所有 node 进程
print('🔴 清理所有 node 进程...')
run(ssh, 'fuser -k 3210/tcp 2>/dev/null || true')
run(ssh, 'pkill -9 -f "node" 2>/dev/null || true')
time.sleep(2)

# 确认端口已释放
out, _ = run(ssh, 'ss -tlnp | grep 3210 || echo "端口已释放"')
print('端口状态:', out)

# 启动服务
print('🚀 启动服务...')
out, _ = run(ssh, 'cd /root/aixin/server && nohup node src/index.js > /tmp/aixin.log 2>&1 & echo PID:$!')
print(out)

time.sleep(4)

# 验证端口
out, _ = run(ssh, 'ss -tlnp | grep 3210')
print('监听:', out)

# 验证接口
print('\n🧪 验证接口...')
out, _ = run(ssh, 'curl -s -o /dev/null -w "%{http_code}" http://localhost:3210/api/portal/stats')
print(f'portal/stats: {out}')

out, _ = run(ssh, """curl -s -X POST http://localhost:3210/api/auth/send-code \
  -H 'Content-Type: application/json' \
  -d '{"email":"hello@example.com"}'""")
print(f'send-code: {out}')

out, _ = run(ssh, """curl -s -X POST http://localhost:3210/api/agents \
  -H 'Content-Type: application/json' \
  -d '{"nickname":"TestUser","email":"hello@example.com","emailCode":""}'""")
print(f'注册(无验证码,应拒绝): {out}')

# 日志尾
out, _ = run(ssh, 'tail -5 /tmp/aixin.log')
print(f'\n服务日志:\n{out}')

ssh.close()
print('\n✅ 完成！')
