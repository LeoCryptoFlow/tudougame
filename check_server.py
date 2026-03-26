# -*- coding: utf-8 -*-
import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.135.138.144', username='root', password='Quan1983@204', timeout=15)

def run(cmd):
    _, o, e = ssh.exec_command(cmd)
    o.channel.recv_exit_status()
    return o.read().decode().strip()

print('=== Node 进程 ===')
print(run('pgrep -a node 2>/dev/null || ps aux | grep node | grep -v grep | head -5'))

print('\n=== PM2 ===')
print(run('pm2 list 2>/dev/null || echo no_pm2'))

print('\n=== /root/aixin ===')
print(run('ls /root/aixin/'))

print('\n=== package.json scripts ===')
print(run('cat /root/aixin/server/package.json | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get(\'scripts\', {}))"'))

print('\n=== 重启 Node 进程 ===')
# 杀掉旧进程，用 pm2 或直接 node 重启
restart = run("""
# 尝试 pm2 重启
if pm2 list 2>/dev/null | grep -q online; then
    pm2 restart all && echo "pm2_restarted"
elif pgrep node > /dev/null; then
    # 获取工作目录，后台重启
    NODE_PID=$(pgrep -f 'node.*index.js' | head -1)
    if [ -n "$NODE_PID" ]; then
        kill $NODE_PID
        sleep 1
        cd /root/aixin/server && nohup node src/index.js > /tmp/aixin.log 2>&1 &
        echo "node_restarted_pid_$!"
    else
        cd /root/aixin/server && nohup node src/index.js > /tmp/aixin.log 2>&1 &
        echo "node_started_pid_$!"
    fi
else
    cd /root/aixin/server && nohup node src/index.js > /tmp/aixin.log 2>&1 &
    echo "node_started_pid_$!"
fi
""")
print(restart)

print('\n等待 3 秒...')
time.sleep(3)

print('\n=== 验证 API ===')
print(run("curl -s -o /dev/null -w 'HTTP %{http_code} TTFB:%{time_starttransfer}s' https://aixin.chat/api/agents"))

print('\n=== 测试注册（新 ID 格式）===')
result = run("""curl -s -X POST https://aixin.chat/api/agents \
  -H 'Content-Type: application/json' \
  -d '{"nickname":"测试格式","password":"test","agentType":"personal","platform":"openclaw","ownerName":"测试"}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('data',{}).get('ax_id','ERROR'), d.get('ok'))" 2>/dev/null""")
print(result)

ssh.close()
