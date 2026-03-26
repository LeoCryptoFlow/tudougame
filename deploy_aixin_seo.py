import paramiko, sys

HOST = '43.135.138.144'
USER = 'root'
PASS = 'Quan1983@204'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASS, timeout=15)
sftp = ssh.open_sftp()

# 上传文件列表
files = [
    ('aixin/website/index.html',   '/root/aixin/website/index.html'),
    ('aixin/website/sitemap.xml',  '/root/aixin/website/sitemap.xml'),
    ('aixin/website/robots.txt',   '/root/aixin/website/robots.txt'),
    ('aixin/deploy/nginx.conf',    '/etc/nginx/conf.d/aixin.conf'),
]

base = '/Users/yunmishu/shengcode/'

for local_rel, remote in files:
    local = base + local_rel
    sftp.put(local, remote)
    print(f'✅ {local_rel} -> {remote}')

sftp.close()

# 检测 nginx 配置并重载
print('\n🔍 检查 nginx 配置...')
stdin, stdout, stderr = ssh.exec_command('nginx -t 2>&1')
result = stdout.read().decode()
print(result)

if 'successful' in result:
    print('🔄 重载 nginx...')
    stdin, stdout, stderr = ssh.exec_command('nginx -s reload')
    stdout.read()
    print('✅ nginx 已重载')
else:
    print('❌ nginx 配置有误，未重载')

# 验证 SEO 文件可访问
print('\n🔍 验证 SEO 文件...')
checks = [
    'curl -s -o /dev/null -w "%{http_code}" https://aixin.chat/robots.txt',
    'curl -s -o /dev/null -w "%{http_code}" https://aixin.chat/sitemap.xml',
    'curl -s -I https://aixin.chat/ 2>/dev/null | head -5',
]
for cmd in checks:
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode().strip()
    print(f'  {cmd.split("aixin.chat")[1] if "aixin.chat" in cmd else cmd}: {out}')

ssh.close()
print('\n🎉 aixin.chat SEO 部署完成！')
