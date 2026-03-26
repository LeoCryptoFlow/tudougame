# -*- coding: utf-8 -*-
import paramiko

host = "43.135.138.144"
user = "root"
passwd = "Quan1983@204"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=passwd, timeout=15)

print("=== Deploy Contact Fix ===\n")

# 1. Upload fixed contact.js
print("1. Uploading fixed contact.js...")
sftp = ssh.open_sftp()
sftp.put("aixin/server/src/modules/contact.js", "/root/aixin/server/src/modules/contact.js")
sftp.close()
print("  OK")

# 2. Restart PM2 service
print("\n2. Restarting aixin-server...")
i, o, e = ssh.exec_command("pm2 restart aixin-server")
o.channel.recv_exit_status()
print(o.read().decode().strip())

# 3. Check status
print("\n3. Checking service status...")
i, o, e = ssh.exec_command("pm2 list | grep aixin-server")
o.channel.recv_exit_status()
print(o.read().decode().strip())

print("\n✅ Contact fix deployed successfully!")
print("\n📝 Fixed issues:")
print("  - Added validation for pending friend requests")
print("  - Improved error messages")
print("  - Better documentation")

ssh.close()
print("\nDone!")
