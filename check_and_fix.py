# -*- coding: utf-8 -*-
import paramiko
import time

host = "43.135.138.144"
user = "root"
passwd = "Quan1983@204"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=passwd, timeout=15)

print("=== 诊断服务器问题 ===\n")

# 1. 检查 Node 进程
print("1. 检查 Node 进程:")
i, o, e = ssh.exec_command("ps aux | grep 'node.*index.js' | grep -v grep")
o.channel.recv_exit_status()
result = o.read().decode().strip()
if result:
    print(f"  ✅ 进程运行中:\n  {result}")
else:
    print("  ❌ 进程未运行！")

# 2. 检查端口
print("\n2. 检查端口 3000:")
i, o, e = ssh.exec_command("ss -tlnp | grep 3000 || netstat -tlnp | grep 3000")
o.channel.recv_exit_status()
print(o.read().decode().strip() or "  ❌ 端口未监听")

# 3. 检查最近的错误日志（如果有）
print("\n3. 检查 Node 进程输出:")
i, o, e = ssh.exec_command("ls -lt /root/aixin/server/*.log 2>&1 | head -5")
o.channel.recv_exit_status()
print(o.read().decode().strip())

# 4. 杀掉所有 node 进程并重启
print("\n4. 重启服务...")
i, o, e = ssh.exec_command("pkill -9 node && sleep 2 && cd /root/aixin/server && nohup node src/index.js > server.log 2>&1 & echo $!")
o.channel.recv_exit_status()
new_pid = o.read().decode().strip()
print(f"  ✅ 新进程 PID: {new_pid}")

# 5. 等待启动
print("\n5. 等待服务启动...")
time.sleep(5)

# 6. 检查日志
print("\n6. 检查启动日志:")
i, o, e = ssh.exec_command("tail -20 /root/aixin/server/server.log 2>&1")
o.channel.recv_exit_status()
log = o.read().decode().strip()
if log:
    print(log)
else:
    print("  (无日志)")

# 7. 测试 API
print("\n7. 测试 API:")
i, o, e = ssh.exec_command("curl -s http://localhost:3000/api/agents | head -c 200")
o.channel.recv_exit_status()
api_result = o.read().decode().strip()
if api_result:
    print(f"  ✅ API 响应: {api_result}...")
else:
    print("  ❌ API 无响应")

ssh.close()
print("\n✅ 诊断完成！")
