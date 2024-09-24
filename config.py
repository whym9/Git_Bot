import os, logging
from dotenv import load_dotenv
import yaml

# Load environment variables
load_dotenv()

# Environment variables
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIS_URL = os.getenv('REDIS_URL')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
REDIRECT_URI = os.getenv('REDIRECT_URI')
# Load configuration from YAML file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

DAILY_RESET_HOUR = config['schedule']['daily_reset_hour']
GITHUB_URL_API = os.getenv('GITHUB_API')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)