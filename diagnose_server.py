# -*- coding: utf-8 -*-
import paramiko

host = "43.135.138.144"
user = "root"
passwd = "Quan1983@204"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=passwd, timeout=15)

print("=== 诊断服务器环境 ===\n")

# 1. 检查工作目录
print("1. 检查 aixin 目录:")
i, o, e = ssh.exec_command("ls -la /root/aixin/ 2>&1")
o.channel.recv_exit_status()
print(o.read().decode().strip())

# 2. 检查 git 状态
print("\n2. Git 状态:")
i, o, e = ssh.exec_command("cd /root/aixin && git status 2>&1")
o.channel.recv_exit_status()
print(o.read().decode().strip())

# 3. 查找 docker
print("\n3. 查找 docker:")
i, o, e = ssh.exec_command("which docker 2>&1 || find /usr -name docker 2>&1 | head -5")
o.channel.recv_exit_status()
print(o.read().decode().strip())

# 4. 检查运行的进程
print("\n4. Node 进程:")
i, o, e = ssh.exec_command("ps aux | grep node | grep -v grep 2>&1")
o.channel.recv_exit_status()
print(o.read().decode().strip())

# 5. 检查端口
print("\n5. 端口 3000:")
i, o, e = ssh.exec_command("netstat -tlnp | grep 3000 2>&1 || ss -tlnp | grep 3000 2>&1")
o.channel.recv_exit_status()
print(o.read().decode().strip())

# 6. 检查 PM2
print("\n6. PM2 状态:")
i, o, e = ssh.exec_command("pm2 list 2>&1")
o.channel.recv_exit_status()
print(o.read().decode().strip())

ssh.close()
print("\n✅ 诊断完成！")
