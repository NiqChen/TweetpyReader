from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
import tweepy
import os
from dotenv import load_dotenv
import logging

# 加载环境变量
load_dotenv()

# 设置 Twitter API 的凭证
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
API_KEY = os.getenv("API_KEY")

# 初始化 API key 认证
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化 FastAPI 应用
app = FastAPI()

# 初始化 Tweepy Client
client = tweepy.Client(bearer_token=bearer_token)

# 定义请求体的模型
class TweetRequest(BaseModel):
    tweet_id: str

# 定义返回的模型
class TweetResponse(BaseModel):
    text: str
    images: list
    created_at: str

# API Key 验证函数
async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid API key"
        )
    return api_key

# API 路由：接 Tweet ID 并返回文本、图片和发布日期
@app.post("/get_tweet", response_model=TweetResponse)
async def get_tweet(data: TweetRequest, api_key: str = Depends(verify_api_key)):
    try:
        logger.info(f"Received request for tweet_id: {data.tweet_id}")

        # 使用更完整的参数设置获取推文
        tweet = client.get_tweet(
            data.tweet_id,
            tweet_fields=[
                'created_at',
                'text',
                'entities',
                'note_tweet'  # 关键字段，用于获取长文本
            ],
            expansions=['attachments.media_keys'],
            media_fields=['url', 'type']
        )
        
        if tweet.data is None:
            logger.error("Tweet not found")
            raise HTTPException(status_code=404, detail="Tweet not found")

        # 获取完整文本
        if hasattr(tweet.data, 'note_tweet'):
            full_text = tweet.data.note_tweet['text']  # 长文本在这里
        else:
            full_text = tweet.data.text

        # 处理媒体 URLs
        media_urls = []
        if hasattr(tweet, 'includes') and 'media' in tweet.includes:
            media_urls = [media.url for media in tweet.includes['media'] 
                         if hasattr(media, 'url') and media.type == 'photo']

        response_data = {
            "text": full_text,
            "images": media_urls,
            "created_at": str(tweet.data.created_at)
        }
        
        logger.info(f"Successfully processed tweet: {response_data}")
        return response_data

    except tweepy.errors.NotFound:
        logger.error("Tweet not found error")
        raise HTTPException(status_code=404, detail="Tweet not found")
    except tweepy.errors.Unauthorized:
        logger.error("Twitter API authentication failed")
        raise HTTPException(status_code=401, detail="Twitter API authentication failed")
    except Exception as e:
        logger.error(f"Internal server error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
