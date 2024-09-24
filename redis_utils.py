import redis
from config import REDIS_URL

redis_client = redis.StrictRedis.from_url(REDIS_URL)

def reset_daily_limits():
    redis_client.flushdb()
    print("Daily limits reset")
