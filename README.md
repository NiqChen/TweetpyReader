# TweetpyReader (推文读取器)

A FastAPI service that fetches tweet content including text, images, and creation date using Twitter API v2.
一个使用 Twitter API v2 获取推文内容（包括文本、图片和创建日期）的 FastAPI 服务。

## Project Structure | 项目结构
```
TweetpyReader/
├── app.py              # Main application file
├── requirements.txt    # Project dependencies
├── Dockerfile         # Docker configuration
├── .env              # Local environment variables (not in git)
└── README.md         # Project documentation
```

## Features | 功能特点
- ✨ Fetch tweet content by ID | 通过ID获取推文内容
- 🔒 Secure API key authentication | 安全的API密钥认证
- 📸 Support for tweet images | 支持推文图片
- ⏰ Include tweet creation time | 包含推文创建时间
- 🚫 Rate limiting protection | 请求频率限制保护

## Prerequisites | 环境要求
- Python 3.8+
- Twitter API v2 Bearer Token
- Docker (optional for deployment)

## Local Development | 本地开发

1. Clone the repository | 克隆仓库
```bash
git clone https://github.com/YourUsername/TweetpyReader.git
cd TweetpyReader
```

2. Install dependencies | 安装依赖
```bash
pip install -r requirements.txt
```

3. Set up environment variables | 设置环境变量
```bash
# Create .env file | 创建 .env 文件
touch .env

# Add these variables | 添加以下变量
TWITTER_BEARER_TOKEN=your_twitter_token
API_KEY=your_api_key
```

4. Run the application | 运行应用
```bash
uvicorn app:app --reload
```

## Deployment | 部署

### Zeabur Deployment | Zeabur 部署
1. Connect your GitHub repository | 连接你的 GitHub 仓库
2. Set environment variables | 设置环境变量:
   - `TWITTER_BEARER_TOKEN`
   - `API_KEY`
3. Deploy | 部署

## API Usage | API 使用方法

### Authentication | 认证
All requests require an API key in the header | 所有请求都需要在头部包含 API 密钥
```
X-API-Key: your_api_key_here
```

### Endpoints | 接口

#### Get Tweet | 获取推文
```http
POST /get_tweet
```

Request | 请求:
```json
{
    "tweet_id": "1234567890"
}
```

Response | 响应:
```json
{
    "text": "Tweet content",
    "images": ["image_url1", "image_url2"],
    "created_at": "2023-11-11T12:00:00Z"
}
```

### n8n Integration | n8n 集成

1. Add HTTP Request node | 添加 HTTP Request 节点
2. Configure as follows | 按如下配置:
```
Method: POST
URL: https://your-api-url/get_tweet
Headers:
  X-API-Key: your_api_key_here
  Content-Type: application/json
Body:
{
    "tweet_id": "={{$json.tweetId}}"
}
```

## Error Codes | 错误代码
- 400: Bad Request | 错误的请求
- 401: Unauthorized | 未授权
- 403: Invalid API Key | 无效的 API 密钥
- 404: Tweet Not Found | 未找到推文
- 429: Too Many Requests | 请求过多
- 500: Server Error | 服务器错误

## Development | 开发

### Adding New Features | 添加新功能
1. Create a new branch | 创建新分支
2. Make changes | 进行修改
3. Submit PR | 提交 PR

### Running Tests | 运行测试
```bash
pytest
```

## Security Notes | 安全注意事项
- Never commit .env file | 永远不要提交 .env 文件
- Rotate API keys regularly | 定期更换 API 密钥
- Use HTTPS in production | 在生产环境使用 HTTPS

## License | 许可证
MIT License

## Support | 支持
For support, please open an issue in the GitHub repository.
如需支持，请在 GitHub 仓库中开一个 issue。