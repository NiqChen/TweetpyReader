from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import tweepy
import os

# 设置 Twitter API 的凭证
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

# 初始化 Tweepy Client
client = tweepy.Client(bearer_token=bearer_token)

# 定义 FastAPI 应用
app = FastAPI()

# 定义请求体的模型
class TweetRequest(BaseModel):
    tweet_id: str

# 定义返回的模型
class TweetResponse(BaseModel):
    text: str
    images: list
    created_at: str

# API 路由：接受 Tweet ID 并返回文本、图片和发布日期
@app.post("/get_tweet", response_model=TweetResponse)
async def get_tweet(data: TweetRequest):
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
