import re
import os
import asyncio
from threading import Thread

from flask import Flask
from pyrogram import Client, filters, idle
from pyrogram.types import Message

from config import API_ID, API_HASH, BOT_TOKEN, CREDIT
import helper  # तुम्हारा helper.py होना चाहिए, जिसमें download_video और send_vid होंगे

app = Flask(__name__)
bot = Client("telegram-drm-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.route("/")
def home():
    return "Bot is running!"

@bot.on_message(filters.command("start") & filters.private)
async def start_cmd(bot, m: Message):
    await m.reply_text(f"Hello {m.from_user.first_name}!\nSend me a .txt file with ClassPlus DRM links.\nUse /help for commands.")

@bot.on_message(filters.command("help") & filters.private)
async def help_cmd(bot, m: Message):
    help_text = (
        "Available Commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help\n"
        "/drmplayer - Get DRM player link from a DRM video URL"
    )
    await m.reply_text(help_text)

@bot.on_message(filters.document & filters.private)
async def handle_txt(bot, m: Message):
    if not m.document.file_name.endswith(".txt"):
        await m.reply_text("Please send a valid .txt file containing video links.")
        return

    filepath = await m.download()
    with open(filepath, "r") as f:
        links = [line.strip() for line in f if line.strip()]

    await m.reply_text(f"Received {len(links)} links. Starting processing...")

    for idx, url in enumerate(links, 1):
        try:
            await m.reply_text(f"Processing video {idx}: {url}")

            # DRM player link for classplusapp DRM videos
            if "classplusapp.com/drm/" in url:
                video_id = url.split("/")[-1].split(".")[0]
                player_link = f"https://playerug.vercel.app/drm?video={video_id}"
                await m.reply_text(f"▶️ DRM Player Link:\n{player_link}")
                continue

            # Simple filename extraction
            name = re.sub(r'\W+', '_', url)[:50]

            # Fixed quality for now
            quality = "720p"

            # Download video using helper (make sure helper.py has this function)
            filename = await helper.download_video(url, f"{name}.mp4")

            caption = f"🎞️ Title: `{name} [{quality}]`\n🔗 Link: {url}\nExtracted By: {CREDIT}"

            await helper.send_vid(bot, m, caption, filename, None, name, None, m.chat.id)

        except Exception as e:
            await m.reply_text(f"Failed to download {url}\nError: {e}")

    os.remove(filepath)
    await m.reply_text("All videos processed!")

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

async def main():
    # Run flask app in separate thread so it doesn't block
    Thread(target=run_flask).start()

    await bot.start()
    print("Bot started successfully!")
    await idle()  # Keep the bot running
    await bot.stop()

if __name__ == "__main__":
    asyncio.run(main())