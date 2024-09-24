from apscheduler.schedulers.asyncio import AsyncIOScheduler
from redis_utils import reset_daily_limits
from config import DAILY_RESET_HOUR

def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(reset_daily_limits, 'cron', hour=DAILY_RESET_HOUR)
    scheduler.start()
