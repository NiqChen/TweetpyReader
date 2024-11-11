from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security.api_key import APIKeyHeader
from dotenv import load_dotenv
import os

load_dotenv()

# 从环境变量获取 API Key
API_KEY = os.getenv("API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

# API Key 验证函数
async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid API key"
        )
    return api_key

# 在每个需要保护的路由上添加验证
@app.post("/get_tweet", response_model=TweetResponse)
async def get_tweet(
    data: TweetRequest, 
    api_key: str = Depends(verify_api_key)  # 添加 API Key 验证
):
    try:
        # Get tweet with expanded fields
        tweet = client.get_tweet(
            data.tweet_id,
            expansions=['attachments.media_keys'],
            media_fields=['url', 'type'],  # Added 'type' field
            tweet_fields=['created_at']
        )
        
        if tweet.data is None:
            raise HTTPException(status_code=404, detail="Tweet not found")

        # Handle case where tweet has no media
        media_urls = []
        if hasattr(tweet, 'includes') and 'media' in tweet.includes:
            media_urls = [media.url for media in tweet.includes['media'] 
                         if hasattr(media, 'url') and media.type == 'photo']

        return {
            "text": tweet.data.text,
            "images": media_urls,
            "created_at": tweet.data.created_at
        }

    except tweepy.errors.NotFound:
        raise HTTPException(status_code=404, detail="Tweet not found")
    except tweepy.errors.Unauthorized:
        raise HTTPException(status_code=401, detail="Twitter API authentication failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["你的n8n域名"],  # 限制特定域名
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

# 添加速率限制
@app.exception_handler(RateLimitExceeded)
async def ratelimit_handler(request, exc):
    return _rate_limit_exceeded_handler(request, exc)
