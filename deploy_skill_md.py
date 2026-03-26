import paramiko

HOST = '43.135.138.144'
USER = 'root'
PASS = 'Quan1983@204'

print('🔌 连接服务器...')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASS, timeout=15)
print('✅ SSH 连接成功')

sftp = ssh.open_sftp()

local_file = '/Users/yunmishu/shengcode/aixin/skill/SKILL.md'

for remote_path in ['/skill/SKILL.md', '/root/aixin/skill/SKILL.md', '/root/skill/SKILL.md']:
    try:
        sftp.put(local_file, remote_path)
        print(f'✅ SKILL.md 上传成功至 {remote_path}')
    except Exception as e:
        print(f'⚠️  {remote_path} 失败: {e}')

# 验证上传
stdin, stdout, stderr = ssh.exec_command('find / -name SKILL.md -path "*/skill/*" 2>/dev/null')
paths = stdout.read().decode().strip()
print(f'\n📂 服务器上的 SKILL.md 位置:\n{paths}')

sftp.close()
ssh.close()
print('\n🎉 部署完成！')
