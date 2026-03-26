# -*- coding: utf-8 -*-
import paramiko

host = "43.135.138.144"
user = "root"
passwd = "Quan1983@204"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=passwd, timeout=15)

# 1. 检查当前版本
print("=== 当前版本 ===")
i, o, e = ssh.exec_command("cd /root/aixin && git log --oneline -1")
o.channel.recv_exit_status()
print(o.read().decode().strip())

# 2. 拉取最新代码
print("\n=== 拉取最新代码 ===")
i, o, e = ssh.exec_command("cd /root/aixin && git pull")
o.channel.recv_exit_status()
print(o.read().decode().strip())

# 3. 检查更新后版本
print("\n=== 更新后版本 ===")
i, o, e = ssh.exec_command("cd /root/aixin && git log --oneline -1")
o.channel.recv_exit_status()
print(o.read().decode().strip())

# 4. 重启后端服务
print("\n=== 重启后端 ===")
i, o, e = ssh.exec_command("docker restart $(docker ps -qf name=aixin) 2>&1 || docker restart $(docker ps -q) 2>&1")
o.channel.recv_exit_status()
print(o.read().decode().strip() or "✅ 重启成功")

# 5. 检查服务状态
print("\n=== 服务状态 ===")
i, o, e = ssh.exec_command("docker ps | grep aixin")
o.channel.recv_exit_status()
print(o.read().decode().strip())

ssh.close()
print("\n✅ 完成！")
