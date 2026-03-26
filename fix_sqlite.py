# -*- coding: utf-8 -*-
import paramiko
import time

host = "43.135.138.144"
user = "root"
passwd = "Quan1983@204"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=passwd, timeout=15)

print("=== 修复 better-sqlite3 模块 ===\n")

# 1. 停止服务
print("1. 停止服务...")
i, o, e = ssh.exec_command("pkill -9 node")
o.channel.recv_exit_status()
print("  ✅ 已停止")

# 2. 重新编译 better-sqlite3
print("\n2. 重新编译 better-sqlite3...")
i, o, e = ssh.exec_command("cd /root/aixin/server && npm rebuild better-sqlite3 2>&1")
o.channel.recv_exit_status()
result = o.read().decode().strip()
print(result[-500:] if len(result) > 500 else result)  # 只显示最后500字符

# 3. 重启服务
print("\n3. 重启服务...")
i, o, e = ssh.exec_command("cd /root/aixin/server && nohup node src/index.js > server.log 2>&1 & echo $!")
o.channel.recv_exit_status()
new_pid = o.read().decode().strip()
print(f"  ✅ 新进程 PID: {new_pid}")

# 4. 等待启动
print("\n4. 等待服务启动...")
time.sleep(5)

# 5. 检查日志
print("\n5. 检查启动日志:")
i, o, e = ssh.exec_command("tail -30 /root/aixin/server/server.log 2>&1")
o.channel.recv_exit_status()
log = o.read().decode().strip()
print(log)

# 6. 检查端口
print("\n6. 检查端口 3000:")
i, o, e = ssh.exec_command("ss -tlnp | grep 3000")
o.channel.recv_exit_status()
port_result = o.read().decode().strip()
if port_result:
    print(f"  ✅ 端口监听中:\n  {port_result}")
else:
    print("  ❌ 端口未监听")

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
print("\n✅ 修复完成！")
