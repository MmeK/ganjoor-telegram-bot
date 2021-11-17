from dotenv import load_dotenv
from os import environ
load_dotenv()

TOKEN = environ.get('TELEGRAM_TOKEN')
URL = environ.get("WEBHOOK_URL")
NAME = "ganjoor_bot"
WEBHOOK = True

WEBHOOK_OPTIONS = {
    'listen': '0.0.0.0',
    'port': 443,
    'url_path': TOKEN,
}
WEBHOOK_URL = f'{URL}/{WEBHOOK_OPTIONS["url_path"]}'
CACHE_TIME = 3600
