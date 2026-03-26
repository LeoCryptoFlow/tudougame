# -*- coding: utf-8 -*-
import paramiko
import time

host = "43.135.138.144"
user = "root"
passwd = "Quan1983@204"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=passwd, timeout=15)

print("=== Test Registration API ===\n")

# 1. Test POST locally
print("1. Test POST request locally:")
cmd = """curl -s -X POST http://localhost:3210/api/agents \
  -H "Content-Type: application/json" \
  -d '{"nickname":"LocalTest","password":"test123","bio":"Local test"}' \
  --max-time 5"""
i, o, e = ssh.exec_command(cmd)
o.channel.recv_exit_status()
result = o.read().decode().strip()
error = e.read().decode().strip()
if result:
    print(f"  Response: {result[:200]}")
else:
    print(f"  No response. Error: {error}")

# 2. Check PM2 logs for errors
print("\n2. Check recent PM2 logs:")
i, o, e = ssh.exec_command("pm2 logs aixin-server --lines 30 --nostream 2>&1 | tail -40")
o.channel.recv_exit_status()
logs = o.read().decode().strip()
if logs:
    print(logs)
else:
    print("  No logs")

# 3. Check if there are any error logs
print("\n3. Check error logs:")
i, o, e = ssh.exec_command("pm2 logs aixin-server --err --lines 20 --nostream 2>&1")
o.channel.recv_exit_status()
err_logs = o.read().decode().strip()
if err_logs:
    print(err_logs)
else:
    print("  No error logs")

ssh.close()
print("\nDone!")
