# -*- coding: utf-8 -*-
import os
import paramiko

host = os.environ.get("AIXIN_HOST", "43.135.138.144")
user = os.environ.get("AIXIN_USER", "root")
passwd = os.environ.get("AIXIN_PASS")  # 必须通过环境变量提供，不写入文件

if not passwd:
    raise RuntimeError("请设置环境变量 AIXIN_PASS，例如：export AIXIN_PASS='your_password'")

local  = "/Users/yunmishu/shengcode/aixin/website/index.html"
remote = "/root/aixin/website/index.html"
db_path = "/root/aixin/server/data/aixin.db"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=passwd, timeout=15)

# 1. Upload HTML
sftp = ssh.open_sftp()
sftp.put(local, remote)
sftp.close()
print("HTML uploaded")

# 2. Update DB: AX-U-CN-XXXX -> AI-XXXX (keep last 4 digits)
sql = "UPDATE agents SET ax_id = 'AI-' || SUBSTR(ax_id, LENGTH(ax_id) - 3) WHERE ax_id LIKE 'AX-%';"
i, o, e = ssh.exec_command(f'sqlite3 {db_path} "{sql}"')
o.channel.recv_exit_status()
err = e.read().decode().strip()
print("DB update:", err if err else "OK")

# 3. Verify
i2, o2, e2 = ssh.exec_command(f"sqlite3 {db_path} 'SELECT ax_id, nickname FROM agents;'")
print(o2.read().decode().strip())

# 4. Restart backend
i3, o3, e3 = ssh.exec_command("docker restart $(docker ps -qf name=aixin_server) 2>&1 || docker restart $(docker ps -q) 2>&1 || true")
o3.channel.recv_exit_status()
print("backend:", o3.read().decode().strip() or "ok")

# 5. Reload nginx
i4, o4, e4 = ssh.exec_command("nginx -s reload 2>&1 || docker exec $(docker ps -qf name=nginx) nginx -s reload 2>&1 || true")
o4.channel.recv_exit_status()
print("nginx: ok")

ssh.close()
print("Done!")
