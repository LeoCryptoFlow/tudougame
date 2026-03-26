# -*- coding: utf-8 -*-
import paramiko

host = "43.135.138.144"
user = "root"
passwd = "Quan1983@204"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=passwd, timeout=15)

print("=== Update Nginx Config ===\n")

# 1. Upload nginx.conf
print("1. Uploading nginx.conf...")
sftp = ssh.open_sftp()
sftp.put("aixin/deploy/nginx.conf", "/etc/nginx/conf.d/aixin.conf")
sftp.close()
print("  OK")

# 2. Test nginx config
print("\n2. Testing nginx config...")
i, o, e = ssh.exec_command("nginx -t")
o.channel.recv_exit_status()
result = o.read().decode().strip()
error = e.read().decode().strip()
print(result if result else error)

# 3. Reload nginx
print("\n3. Reloading nginx...")
i, o, e = ssh.exec_command("nginx -s reload")
o.channel.recv_exit_status()
print("  OK")

# 4. Test POST request
print("\n4. Testing POST request...")
import time
time.sleep(2)
cmd = """curl -s -X POST http://localhost:3210/api/agents \
  -H "Content-Type: application/json" \
  -d '{"nickname":"NginxTest","password":"test123"}' \
  --max-time 10"""
i, o, e = ssh.exec_command(cmd)
o.channel.recv_exit_status()
result = o.read().decode().strip()
if result:
    print(f"  Local POST OK: {result[:100]}...")
else:
    print("  No response")

ssh.close()
print("\nDone!")
