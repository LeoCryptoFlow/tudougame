# 如何获取币安 API 密钥 🔑

本指南将帮助您在币安（Binance）交易所获取API密钥，以便使用本量化交易系统进行实盘交易。

## ⚠️ 重要说明

**当前系统仅使用公开API（不需要密钥）**
- 本量化交易系统目前仅用于**数据获取**和**模拟回测**
- 获取历史价格、实时行情等公开数据**不需要API密钥**
- 只有进行**实盘交易**（下单、查询账户等）才需要API密钥

## 📋 获取币安API密钥步骤

### 第一步：注册币安账户

1. 访问币安官网：https://www.binance.com
2. 点击右上角"注册"按钮
3. 使用邮箱或手机号完成注册
4. 完成身份验证（KYC）

### 第二步：启用双重验证（2FA）

⚠️ **必须先启用2FA才能创建API密钥**

1. 登录币安账户
2. 点击右上角头像 → "安全"
3. 找到"双重验证（2FA）"
4. 选择并启用以下一种或多种方式：
   - Google Authenticator（推荐）
   - 短信验证
   - 邮箱验证

### 第三步：创建API密钥

1. **进入API管理页面**
   - 点击右上角头像
   - 选择"API管理"
   - 或直接访问：https://www.binance.com/zh-CN/my/settings/api-management

2. **创建新的API密钥**
   - 点击"创建API"按钮
   - 输入API标签（例如："量化交易系统"）
   - 完成2FA验证（输入验证码）

3. **保存API信息**
   ```
   API Key：    [您的API密钥，类似于用户名]
   Secret Key： [您的密钥，类似于密码] ⚠️ 只显示一次，务必保存！
   ```
   
   ⚠️ **Secret Key只在创建时显示一次，请立即保存到安全的地方！**

4. **配置API权限**（根据需求勾选）
   - ☑️ 启用现货及杠杆交易
   - ☐ 启用期货（如果需要）
   - ☑️ 启用读取（查看账户信息）
   - ☐ 启用提现（不推荐，安全考虑）

5. **IP访问限制**（强烈推荐）
   - 选择"限制访问受信任的IP"
   - 添加您的服务器或电脑的IP地址
   - 这样可以防止API被盗用

### 第四步：测试API连接

创建测试文件验证API密钥是否有效：

```python
# test_api.py
from binance.client import Client

api_key = '您的API_KEY'
api_secret = '您的SECRET_KEY'

# 创建客户端
client = Client(api_key, api_secret)

# 测试连接
try:
    account = client.get_account()
    print("✅ API连接成功！")
    print(f"账户状态: {account['accountType']}")
except Exception as e:
    print(f"❌ API连接失败: {e}")
```

## 🔐 安全最佳实践

### 1. **永远不要泄露您的API密钥**
   - ❌ 不要上传到GitHub等公开仓库
   - ❌ 不要与他人分享
   - ❌ 不要在不安全的设备上使用

### 2. **使用环境变量存储密钥**

创建 `.env` 文件（已在.gitignore中）：
```bash
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

在代码中读取：
```python
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')
```

### 3. **设置IP白名单**
   - 只允许特定IP访问您的API
   - 定期更新IP白名单

### 4. **最小权限原则**
   - 只启用必需的权限
   - 不要启用提现权限（除非绝对必要）
   - 定期审查API权限设置

### 5. **定期更换密钥**
   - 每3-6个月更换一次API密钥
   - 如怀疑泄露，立即删除并创建新密钥

### 6. **使用测试网**
   开始时建议使用币安测试网：
   - 测试网地址：https://testnet.binance.vision/
   - 免费获取测试API
   - 使用虚拟资金测试策略

## 📚 API使用示例

### 安装币安Python SDK

```bash
pip install python-binance
```

### 基础使用示例

```python
from binance.client import Client
import os

# 从环境变量读取密钥
api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')

# 创建客户端
client = Client(api_key, api_secret)

# 获取账户信息
account = client.get_account()
print(f"账户类型: {account['accountType']}")

# 获取账户余额
balances = client.get_account()['balances']
for balance in balances:
    if float(balance['free']) > 0:
        print(f"{balance['asset']}: {balance['free']}")

# 获取最新价格
btc_price = client.get_symbol_ticker(symbol="BTCUSDT")
print(f"BTC价格: ${btc_price['price']}")

# 下单（测试订单，不会真正执行）
order = client.create_test_order(
    symbol='BTCUSDT',
    side=Client.SIDE_BUY,
    type=Client.ORDER_TYPE_LIMIT,
    timeInForce=Client.TIME_IN_FORCE_GTC,
    quantity=0.001,
    price='50000'
)
```

## 🔄 集成到本项目

如果您想在本量化交易系统中使用API进行实盘交易，需要：

1. **安装额外依赖**
   ```bash
   pip install python-binance python-dotenv
   ```

2. **创建配置文件**
   ```bash
   # 在项目根目录创建 .env 文件
   echo "BINANCE_API_KEY=your_key" >> .env
   echo "BINANCE_API_SECRET=your_secret" >> .env
   ```

3. **修改代码以支持实盘交易**
   - 需要修改 `data_fetcher.py` 以支持认证API
   - 添加订单执行模块
   - 实现风险管理系统

## ❓ 常见问题

### Q1: 我需要API密钥才能使用这个系统吗？
**A:** 不需要！当前系统只使用公开API获取市场数据，不需要API密钥。

### Q2: API密钥丢失了怎么办？
**A:** Secret Key一旦丢失无法找回，只能删除旧密钥并创建新的。

### Q3: API有请求限制吗？
**A:** 是的，币安有请求频率限制：
- 普通API: 1200请求/分钟
- 权重限制: 参考币安API文档

### Q4: 如何测试API是否正常？
**A:** 使用测试网或创建测试订单（不会真正执行）。

### Q5: API密钥被盗用怎么办？
**A:** 立即：
1. 登录币安账户
2. 删除被盗用的API密钥
3. 启用账户安全措施
4. 检查账户交易记录
5. 联系币安客服

## 📖 相关资源

- 币安API官方文档：https://binance-docs.github.io/apidocs/spot/cn/
- Python-Binance文档：https://python-binance.readthedocs.io/
- 币安API常见问题：https://www.binance.com/zh-CN/support/faq
- 币安测试网：https://testnet.binance.vision/

## ⚖️ 免责声明

- 本指南仅供学习参考
- 使用API进行实盘交易有风险
- 请确保了解所有风险后再进行交易
- 作者不对任何损失负责

---

**📌 记住：当前系统不需要API密钥就能运行！只有需要实盘交易时才需要。**
