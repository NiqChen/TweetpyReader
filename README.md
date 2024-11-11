# TweetpyReader
# 推文读取器

A FastAPI application that uses Tweepy to fetch tweet content including text, images, and creation date.
一个使用 Tweepy 获取推文内容（包括文本、图片和创建日期）的 FastAPI 应用程序。

## Features | 功能
- Fetch tweets by username | 通过用户名获取推文
- Get tweet text, images, and creation date | 获取推文文本、图片和创建日期
- Asynchronous API endpoints | 异步 API 接口
- Error handling and rate limiting | 错误处理和速率限制
- API Key authentication | API 密钥认证
- Rate limiting protection | 请求频率限制保护
- CORS protection | CORS 跨域保护

## Prerequisites | 前置要求
- Python 3.8+
- Twitter API v2 access (Bearer Token) | Twitter API v2 访问权限（Bearer Token）
- FastAPI
- Tweepy
- python-dotenv

## Setup | 设置

1. Install dependencies | 安装依赖:
   ```bash
   pip install -r requirements.txt
   ```

2. Create and configure .env file | 创建并配置 .env 文件:
   ```plaintext
   TWITTER_BEARER_TOKEN=your_twitter_token
   API_KEY=your_complex_api_key
   ```

3. Generate API Key | 生成 API 密钥:
   ```python
   import secrets
   print(secrets.token_urlsafe(32))
   ```

## Usage | 使用方法

1. Start the server | 启动服务器:
   ```bash
   uvicorn main:app --reload
   ```

2. Access API documentation | 访问 API 文档:
   ```
   http://localhost:8000/docs
   ```

## API Endpoints | API 接口

### POST /get_tweet
Fetches tweet content by ID | 通过推文 ID 获取内容

Headers | 请求头:
- X-API-Key: Your API key | 你的 API 密钥

Request Body | 请求体:
```json
{
    "tweet_id": "tweet_id_here"
}
```

Response | 返回:
```json
{
    "text": "tweet_text",
    "images": ["image_url1", "image_url2"],
    "created_at": "timestamp"
}
```

## Security Features | 安全特性
- API Key Authentication | API 密钥认证
- Rate Limiting | 请求频率限制
- CORS Protection | CORS 跨域保护
- Request Logging | 请求日志记录
- Error Handling | 错误处理

## Error Handling | 错误处理
- 400: Bad Request - Invalid parameters | 无效参数
- 401: Unauthorized - Invalid API Key | 无效的 API 密钥
- 403: Forbidden - Invalid permissions | 权限不足
- 404: Not Found - Tweet not found | 未找到推文