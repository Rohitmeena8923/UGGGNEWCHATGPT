# Telegram DRM Player Bot

A Telegram bot to generate DRM player links for Classplus videos.

## Setup
1. `cp .env.example .env`
2. Fill in your tokens and OWNER_ID.
3. `pip install -r requirements.txt`
4. Deploy to Render (automatic environment support) or locally: `python main.py`.

### Usage
- `/start` – Greet
- `/drmplayer <url>` – Get player link for one URL
- Upload `.txt` (private) with multiple links – auto generates links

✅ Only the OWNER can use batch uploads.

Enjoy! 🎬