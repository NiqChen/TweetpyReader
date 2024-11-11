# TweetpyReader
# 推文读取器

A FastAPI application that uses Tweepy to fetch tweet content including text, images, and creation date.
一个使用 Tweepy 获取推文内容（包括文本、图片和创建日期）的 FastAPI 应用程序。

## Features | 功能
- Fetch tweets by username | 通过用户名获取推文
- Get tweet text, images, and creation date | 获取推文文本、图片和创建日期
- Asynchronous API endpoints | 异步 API 接口
- Error handling and rate limiting | 错误处理和速率限制

## Prerequisites | 前置要求
- Python 3.8+
- Twitter API v2 access (Bearer Token) | Twitter API v2 访问权限（Bearer Token）
- FastAPI
- Tweepy

## Setup | 设置

1. Install dependencies | 安装依赖:
   ```
   pip install -r requirements.txt
   ```

2. Set environment variables | 设置环境变量:
   - TWITTER_BEARER_TOKEN: Your Twitter API bearer token | 你的 Twitter API 访问令牌

## Usage | 使用方法

1. Start the server | 启动服务器:
   ```
   uvicorn main:app --reload
   ```

2. Access API documentation | 访问 API 文档:
   ```
   http://localhost:8000/docs
   ```

## API Endpoints | API 接口

### GET /tweets/{username}
Fetches recent tweets from a specified user | 获取指定用户的最近推文

Parameters | 参数:
- username: Twitter username without @ | Twitter 用户名（不带@）

Response | 返回:
```json
{
    "tweets": [
        {
            "id": "tweet_id",
            "text": "tweet_text",
            "created_at": "timestamp",
            "images": ["image_url1", "image_url2"]
        }
    ]
}
```

### GET /tweets/search/{query}
Searches tweets by keyword | 通过关键词搜索推文

Parameters | 参数:
- query: Search keyword | 搜索关键词

## Error Handling | 错误处理
- 400: Bad Request - Invalid parameters | 无效参数
- 404: Not Found - User or tweets not found | 未找到用户或推文
- 429: Too Many Requests - Rate limit exceeded | 超出速率限制
- 500: Internal Server Error - Server-side issues | 服务器端问题

## Contributing | 贡献
Pull requests are welcome. For major changes, please open an issue first.
欢迎提交 Pull Request。如需重大更改，请先开 Issue 讨论。

## License | 许可证
MIT License