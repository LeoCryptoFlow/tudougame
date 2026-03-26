# -*- coding: utf-8 -*-
import paramiko
import time

host = "43.135.138.144"
user = "root"
passwd = "Quan1983@204"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=passwd, timeout=15)

print("=== Test POST Speed ===\n")

# 1. Test local POST speed
print("1. Test local POST (should be fast):")
start = time.time()
cmd = """curl -s -w "\\nTime: %{time_total}s\\n" -X POST http://localhost:3210/api/agents \
  -H "Content-Type: application/json" \
  -d '{"nickname":"SpeedTest1","password":"test"}' \
  --max-time 10"""
i, o, e = ssh.exec_command(cmd)
o.channel.recv_exit_status()
result = o.read().decode().strip()
elapsed = time.time() - start
print(f"  Result: {result[:150]}")
print(f"  Total time: {elapsed:.2f}s\n")

# 2. Test HTTPS POST from server
print("2. Test HTTPS POST from server (through Nginx):")
start = time.time()
cmd = """curl -s -w "\\nTime: %{time_total}s\\n" -X POST https://aixin.chat/api/agents \
  -H "Content-Type: application/json" \
  -d '{"nickname":"SpeedTest2","password":"test"}' \
  --max-time 15 -k"""
i, o, e = ssh.exec_command(cmd)
o.channel.recv_exit_status()
result = o.read().decode().strip()
elapsed = time.time() - start
print(f"  Result: {result[:150]}")
print(f"  Total time: {elapsed:.2f}s\n")

# 3. Check server load
print("3. Check server load:")
i, o, e = ssh.exec_command("uptime && free -h")
o.channel.recv_exit_status()
print(o.read().decode().strip())

# 4. Check Node.js process
print("\n4. Check Node.js process:")
i, o, e = ssh.exec_command("ps aux | grep 'node.*3210' | grep -v grep")
o.channel.recv_exit_status()
print(o.read().decode().strip())

ssh.close()
print("\nDone!")
