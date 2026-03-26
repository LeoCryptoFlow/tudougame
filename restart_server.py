#!/usr/bin/env python3
import paramiko, time

HOST = '43.135.138.144'
USER = 'root'
PASS = 'Quan1983@204'

def run(ssh, cmd, timeout=30):
    _, o, e = ssh.exec_command(cmd, timeout=timeout)
    o.channel.recv_exit_status()
    out = o.read().decode().strip()
    err = e.read().decode().strip()
    return out, err

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASS, timeout=15)
print('✅ SSH 连接成功')

# 1. 找进程管理器
out, _ = run(ssh, 'export PATH=$PATH:/usr/local/bin:/usr/bin && pm2 list 2>&1 | head -20')
print('PM2:\n', out)

out, _ = run(ssh, 'ps aux | grep "node.*index" | grep -v grep')
print('Node 进程:', out)

# 2. 找到服务路径和启动方式
out, _ = run(ssh, 'ls /root/aixin/server/src/api/routes.js && echo "路径OK"')
print(out)

# 3. 重启 PM2 服务
out, _ = run(ssh, 'export PATH=$PATH:/usr/local/bin && pm2 restart all 2>&1 || true')
print('PM2 restart:', out)

# 4. 用 kill+启动方式
out, _ = run(ssh, 'pgrep -f "node.*index" | head -5')
pids = out.strip()
print('Node PIDs:', pids)

if pids:
    for pid in pids.split('\n'):
        run(ssh, f'kill {pid.strip()} 2>/dev/null || true')
    print('已 kill 旧进程')
    time.sleep(1)

# 5. 找到启动命令
out, _ = run(ssh, 'cat /root/aixin/server/package.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get(\'scripts\',{}))"')
print('启动脚本:', out)

out, _ = run(ssh, 'ls /root/aixin/server/src/index.js && cat /root/aixin/server/src/index.js | head -5')
print('index.js 存在:', out[:100])

# 6. 在后台重启服务
out, _ = run(ssh, 'cd /root/aixin/server && nohup node src/index.js > /tmp/aixin.log 2>&1 & sleep 3 && echo started_pid:$!')
print('启动结果:', out)

time.sleep(3)

# 7. 验证新接口
for port in [3210, 3000]:
    out, _ = run(ssh, f'curl -s -X POST http://localhost:{port}/api/auth/send-code -H "Content-Type: application/json" -d \'{{"email":"test@qq.com"}}\' 2>/dev/null')
    if out and 'Cannot POST' not in out and '000' not in out:
        print(f'✅ port {port} send-code: {out}')
        break
    else:
        print(f'port {port}: {out[:80] if out else "无响应"}')

# 8. 查看日志
out, _ = run(ssh, 'tail -20 /tmp/aixin.log 2>/dev/null')
print('服务日志:\n', out)

ssh.close()
print('Done')
