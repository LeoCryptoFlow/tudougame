# -*- coding: utf-8 -*-
import paramiko

host = "43.135.138.144"
user = "root"
passwd = "Quan1983@204"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=passwd, timeout=15)

print("=== Check PM2 Status ===\n")

# 1. PM2 list
print("1. PM2 process list:")
i, o, e = ssh.exec_command("pm2 list")
o.channel.recv_exit_status()
print(o.read().decode().strip())

# 2. View logs
print("\n2. Recent logs:")
i, o, e = ssh.exec_command("pm2 logs aixin-server --lines 20 --nostream")
o.channel.recv_exit_status()
print(o.read().decode().strip())

# 3. Check port
print("\n3. Port listening:")
i, o, e = ssh.exec_command("ss -tlnp | grep 3210")
o.channel.recv_exit_status()
result = o.read().decode().strip()
print(result if result else "  Port not listening")

# 4. Test local API
print("\n4. Test local API:")
i, o, e = ssh.exec_command("curl -s http://localhost:3210/api/agents | head -c 100")
o.channel.recv_exit_status()
print(o.read().decode().strip() or "  No response")

ssh.close()
print("\nDone!")
