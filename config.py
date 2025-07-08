import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID", "27775431"))
API_HASH = os.getenv("API_HASH", "b70bb1d45a1d05236671d4cc615e40f9")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
CREDIT = os.getenv("CREDIT", "Lucifer ❤️")