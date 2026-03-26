# -*- coding: utf-8 -*-
import paramiko

host = "43.135.138.144"
user = "root"
passwd = "Quan1983@204"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=passwd, timeout=15)

print("=== Upload Optimized Skill ===\n")

# 1. Create directory if not exists
print("1. Creating skill directory...")
i, o, e = ssh.exec_command("mkdir -p /root/aixin/skill")
o.channel.recv_exit_status()
print("  OK")

# 2. Upload skill file
print("\n2. Uploading aixin-skill.py...")
sftp = ssh.open_sftp()
sftp.put("aixin/skill/aixin-skill.py", "/root/aixin/skill/aixin-skill.py")
sftp.close()
print("  OK")

# 3. Verify file
print("\n3. Verify uploaded file:")
i, o, e = ssh.exec_command("head -30 /root/aixin/skill/aixin-skill.py | grep -E '(SERVER_URL|session|HTTPAdapter)'")
o.channel.recv_exit_status()
print(o.read().decode().strip())

print("\n✅ Skill file uploaded successfully!")
print("\n📝 Changes made:")
print("  - Changed SERVER_URL from HTTP to HTTPS")
print("  - Changed from IP (43.135.138.144) to domain (aixin.chat)")
print("  - Added connection pool with session object")
print("  - All requests now use session for connection reuse")
print("\n🚀 OpenClaw users should now experience faster registration!")

ssh.close()
print("\nDone!")
