import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID", "1234567"))
API_HASH = os.getenv("API_HASH", "your_api_hash_here")
BOT_TOKEN = os.getenv("BOT_TOKEN", "1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ")
CREDIT = os.getenv("CREDIT", "YourName")