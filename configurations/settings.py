from dotenv import load_dotenv
from os import environ
load_dotenv()

TOKEN = environ.get('TELEGRAM_TOKEN')
URL = environ.get("WEBHOOK_URL")
PORT = int(environ.get('PORT', 8443))

NAME = "ganjoor_bot"
WEBHOOK = True
WEBHOOK_URL = f'{URL}/{TOKEN}'

WEBHOOK_OPTIONS = {
    'listen': '0.0.0.0',
    'port': PORT,
    'url_path': TOKEN,
    'webhook_url': WEBHOOK_URL
}
CACHE_TIME = 3600
