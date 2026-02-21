#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { TwitterApi } from 'twitter-api-v2';
import dotenv from 'dotenv';

dotenv.config();

const BEARER_TOKEN = process.env.TWITTER_BEARER_TOKEN;

if (!BEARER_TOKEN) {
  console.error('错误: 请在 .env 文件中设置 TWITTER_BEARER_TOKEN');
  process.exit(1);
}

// 创建只读Twitter客户端
const twitterClient = new TwitterApi(BEARER_TOKEN);
const readOnlyClient = twitterClient.readOnly;

// 创建MCP服务器
const server = new Server(
  {
    name: 'twitter-mcp-server',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// 定义工具列表
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'search_tweets',
        description: '搜索推文。可以按关键词、用户、标签等搜索最近的推文',
        inputSchema: {
          type: 'object',
          properties: {
            query: {
              type: 'string',
              description: '搜索查询（例如: "AI" 或 "from:elonmusk" 或 "#bitcoin"）',
            },
            max_results: {
              type: 'number',
              description: '返回的最大结果数（10-100，默认10）',
              default: 10,
            },
          },
          required: ['query'],
        },
      },
      {
        name: 'get_user_info',
        description: '获取推特用户的详细信息（用户名、简介、粉丝数等）',
        inputSchema: {
          type: 'object',
          properties: {
            username: {
              type: 'string',
              description: '推特用户名（不含@符号）',
            },
          },
          required: ['username'],
        },
      },
      {
        name: 'get_user_tweets',
        description: '获取指定用户的最新推文',
        inputSchema: {
          type: 'object',
          properties: {
            username: {
              type: 'string',
              description: '推特用户名（不含@符号）',
            },
            max_results: {
              type: 'number',
              description: '返回的最大推文数（5-100，默认10）',
              default: 10,
            },
          },
          required: ['username'],
        },
      },
      {
        name: 'get_trending_topics',
        description: '获取指定地区的热门话题',
        inputSchema: {
          type: 'object',
          properties: {
            woeid: {
              type: 'number',
              description: 'Yahoo! Where On Earth ID (例如: 1 为全球, 23424977 为美国)',
              default: 1,
            },
          },
        },
      },
      {
        name: 'analyze_tweet_sentiment',
        description: '分析推文的情感倾向（简单的情感分析）',
        inputSchema: {
          type: 'object',
          properties: {
            text: {
              type: 'string',
              description: '要分析的推文文本',
            },
          },
          required: ['text'],
        },
      },
    ],
  };
});

// 简单的情感分析函数
function analyzeSentiment(text) {
  const positiveWords = ['好', '棒', '喜欢', '爱', '优秀', '完美', '太棒了', 'good', 'great', 'love', 'awesome', 'amazing', 'excellent', 'happy', 'wonderful'];
  const negativeWords = ['坏', '差', '讨厌', '恨', '糟糕', '失望', 'bad', 'terrible', 'hate', 'awful', 'horrible', 'sad', 'angry', 'disappointed'];
  
  const lowerText = text.toLowerCase();
  let score = 0;
  
  positiveWords.forEach(word => {
    if (lowerText.includes(word)) score++;
  });
  
  negativeWords.forEach(word => {
    if (lowerText.includes(word)) score--;
  });
  
  if (score > 0) return '积极 (Positive)';
  if (score < 0) return '消极 (Negative)';
  return '中性 (Neutral)';
}

// 处理工具调用
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case 'search_tweets': {
        const { query, max_results = 10 } = args;
        const tweets = await readOnlyClient.v2.search(query, {
          max_results: Math.min(Math.max(max_results, 10), 100),
          'tweet.fields': ['created_at', 'public_metrics', 'author_id'],
          'user.fields': ['username', 'name'],
          expansions: ['author_id'],
        });

        const results = [];
        for await (const tweet of tweets) {
          const author = tweets.includes.users.find(u => u.id === tweet.author_id);
          results.push({
            id: tweet.id,
            text: tweet.text,
            author: author ? `${author.name} (@${author.username})` : '未知用户',
            created_at: tweet.created_at,
            metrics: {
              likes: tweet.public_metrics?.like_count || 0,
              retweets: tweet.public_metrics?.retweet_count || 0,
              replies: tweet.public_metrics?.reply_count || 0,
            },
          });
        }

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(results, null, 2),
            },
          ],
        };
      }

      case 'get_user_info': {
        const { username } = args;
        const user = await readOnlyClient.v2.userByUsername(username, {
          'user.fields': ['description', 'public_metrics', 'created_at', 'verified'],
        });

        const userInfo = {
          id: user.data.id,
          username: user.data.username,
          name: user.data.name,
          description: user.data.description,
          verified: user.data.verified || false,
          created_at: user.data.created_at,
          metrics: {
            followers: user.data.public_metrics?.followers_count || 0,
            following: user.data.public_metrics?.following_count || 0,
            tweets: user.data.public_metrics?.tweet_count || 0,
          },
        };

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(userInfo, null, 2),
            },
          ],
        };
      }

      case 'get_user_tweets': {
        const { username, max_results = 10 } = args;
        const user = await readOnlyClient.v2.userByUsername(username);
        const tweets = await readOnlyClient.v2.userTimeline(user.data.id, {
          max_results: Math.min(Math.max(max_results, 5), 100),
          'tweet.fields': ['created_at', 'public_metrics'],
        });

        const results = [];
        for await (const tweet of tweets) {
          results.push({
            id: tweet.id,
            text: tweet.text,
            created_at: tweet.created_at,
            metrics: {
              likes: tweet.public_metrics?.like_count || 0,
              retweets: tweet.public_metrics?.retweet_count || 0,
              replies: tweet.public_metrics?.reply_count || 0,
            },
          });
        }

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(results, null, 2),
            },
          ],
        };
      }

      case 'get_trending_topics': {
        const { woeid = 1 } = args;
        
        // 注意: Twitter API v2 不再直接支持趋势API（需要企业级访问）
        // 这里返回一个提示信息
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                message: '趋势API需要Twitter企业级访问权限。建议使用 search_tweets 搜索热门话题标签。',
                suggestion: '尝试搜索: #trending 或其他热门标签',
              }, null, 2),
            },
          ],
        };
      }

      case 'analyze_tweet_sentiment': {
        const { text } = args;
        const sentiment = analyzeSentiment(text);
        
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                text: text,
                sentiment: sentiment,
                note: '这是一个基于关键词的简单情感分析',
              }, null, 2),
            },
          ],
        };
      }

      default:
        throw new Error(`未知工具: ${name}`);
    }
  } catch (error) {
    return {
      content: [
        {
          type: 'text',
          text: `错误: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
});

// 启动服务器
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('推特MCP服务器已启动');
}

main().catch((error) => {
  console.error('服务器错误:', error);
  process.exit(1);
});
