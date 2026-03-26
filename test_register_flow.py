import sys
import os

# 将项目目录加入包路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'aixin/skill')))
try:
    from aixin.skill import aixin_skill
except Exception as e:
    import builtins
    builtins.__import__('sys').path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'aixin/skill')))
    aixin_skill = __import__('aixin-skill')

# 重置本地存储，防止用旧的号
local_store = os.path.expanduser("~/.aixin/profile.json")
if os.path.exists(local_store):
    os.remove(local_store)
aixin_skill.LOCAL_STORE = "/tmp/aixin_test_profile.json"
if os.path.exists("/tmp/aixin_test_profile.json"):
    os.remove("/tmp/aixin_test_profile.json")

skill = aixin_skill.AIXinSkill()

print("1. 触发注册")
res1 = skill.handle_input("/aixin 注册", "我是测试助理")
print("返回:", res1)

print("\n2. 回复邮箱")
if type(res1) is dict and res1.get('type') == 'interactive':
    res2 = res1['callback']({"email": "test@aixin.chat"})
    print("返回:", res2)
    
    print("\n3. 回复完整的注册信息 (伪造验证码，因为我们无法收到邮件，但后端会报错邮箱不正确或验证码错误，我们只看逻辑是否走到后端)")
    if type(res2) is dict and res2.get('type') == 'interactive':
        # 故意填错验证码
        res3 = res2['callback']({
            "emailCode": "000000",
            "nickname": "TestBot",
            "owner_name": "TestOwner",
            "password": "123",
            "bio": "测试注册流"
        })
        print("返回:", res3)
