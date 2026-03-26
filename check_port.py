# -*- coding: utf-8 -*-
import paramiko
import time

host = "43.135.138.144"
user = "root"
passwd = "Quan1983@204"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=passwd, timeout=15)

print("=== 检查端口占用 ===\n")

# 1. 检查端口 3210
print("1. 端口 3210 占用情况:")
i, o, e = ssh.exec_command("ss -tlnp | grep 3210 || netstat -tlnp | grep 3210")
o.channel.recv_exit_status()
result = o.read().decode().strip()
if result:
    print(result)
else:
    print("  端口未被占用")

# 2. 检查所有 node 进程
print("\n2. 所有 node 进程:")
i, o, e = ssh.exec_command("ps aux | grep node | grep -v grep")
o.channel.recv_exit_status()
print(o.read().decode().strip() or "  无 node 进程")

# 3. 检查 index.js 中的端口配置
print("\n3. 检查 index.js 端口配置:")
i, o, e = ssh.exec_command("grep -n 'listen\\|3210\\|3000\\|PORT' /root/aixin/server/src/index.js | head -10")
o.channel.recv_exit_status()
print(o.read().decode().strip())

# 4. 杀掉占用端口的进程
print("\n4. 清理端口占用...")
i, o, e = ssh.exec_command("fuser -k 3210/tcp 2>&1 && fuser -k 3000/tcp 2>&1 && pkill -9 node 2>&1")
o.channel.recv_exit_status()
print(o.read().decode().strip() or "  OK")

# 5. 等待并重启
print("\n5. 重启服务...")
i, o, e = ssh.exec_command("sleep 3 && cd /root/aixin/server && nohup node src/index.js > server.log 2>&1 & echo $!")
o.channel.recv_exit_status()
new_pid = o.read().decode().strip()
print(f"  New PID: {new_pid}")

time.sleep(5)

# 6. 检查启动状态
print("\n6. 检查启动日志:")
i, o, e = ssh.exec_command("tail -30 /root/aixin/server/server.log")
o.channel.recv_exit_status()
log = o.read().decode().strip()
print(log[-400:] if len(log) > 400 else log)

# 7. 测试 API
print("\n7. 测试 API:")
i, o, e = ssh.exec_command("curl -s http://localhost:3000/api/agents | head -c 100")
o.channel.recv_exit_status()
api_result = o.read().decode().strip()
if api_result:
    print(f"  API OK: {api_result}...")
else:
    print("  API no response")

ssh.close()
print("\nDone!")
