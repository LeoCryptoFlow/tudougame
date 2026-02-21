# Twitter MCP Server

一个用于Twitter/X的Model Context Protocol (MCP)服务器，提供搜索推文和获取用户信息的功能。

## 功能特性

- 🔍 **搜索推文**: 根据关键词搜索最新的推文
- 👤 **获取用户信息**: 通过用户名获取Twitter用户的详细信息

## 安装步骤

### 1. 安装依赖

```bash
cd twitter-mcp-server
npm install
```

### 2. 配置Twitter API凭证

1. 访问 [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. 创建一个应用并获取Bearer Token
3. 复制 `.env.example` 为 `.env`:
   ```bash
   cp .env.example .env
   ```
4. 编辑 `.env` 文件，填入你的真实凭证:
   ```
   TWITTER_BEARER_TOKEN=your_actual_bearer_token_here
   ```

### 3. 配置到VSCode/Cline

在VSCode的Cline扩展配置中添加此MCP服务器：

1. 打开VSCode设置
2. 搜索 "MCP Servers"
3. 添加服务器配置:

```json
{
  "mcpServers": {
    "twitter": {
      "command": "node",
      "args": ["/Users/yunmishu/shengcode/twitter-mcp-server/index.js"]
    }
  }
}
```

## 使用方法

配置完成后，您可以在Cline中使用以下工具：

### 搜索推文
- 工具名: `search_tweets`
- 参数: `query` (搜索关键词), `max_results` (可选，默认10条)

### 获取用户信息
- 工具名: `get_user_info`
- 参数: `username` (Twitter用户名)

## 示例

```javascript
// 搜索推文
{
  "query": "AI技术",
  "max_results": 20
}

// 获取用户信息
{
  "username": "elonmusk"
}
```

## 技术栈

- Node.js (ESM模块)
- @modelcontextprotocol/sdk
- twitter-api-v2
- dotenv

## 注意事项

- ⚠️ **重要**: 不要将 `.env` 文件提交到版本控制系统
- 确保您的Twitter API Bearer Token有足够的权限
- Twitter API有速率限制，请合理使用

## 开发

测试服务器是否正常运行：

```bash
node index.js
```

如果配置正确，服务器将启动并等待MCP客户端连接。

## License

ISC
