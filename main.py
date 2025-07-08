import re
import asyncio
import os
from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN, CREDIT
import helper
from flask import Flask

app = Flask(__name__)

bot = Client("telegram-drm-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.route("/")
def home():
    return "Bot is running!"

@bot.on_message(filters.command("start") & filters.private)
async def start_cmd(bot, m: Message):
    await m.reply_text(f"Hello {m.from_user.first_name}!\nSend me a .txt file containing ClassPlus DRM links to download videos one by one.\nUse /help for commands.")

@bot.on_message(filters.command("help") & filters.private)
async def help_cmd(bot, m: Message):
    help_text = """
Available Commands:
/start - Start bot
/help - Show this help
/drmplayer - Send DRM player link from a DRM video URL
"""
    await m.reply_text(help_text)

@bot.on_message(filters.document & filters.private)
async def doc_handler(bot, m: Message):
    if not m.document.file_name.endswith(".txt"):
        await m.reply_text("Please send a valid .txt file with video links.")
        return

    f = await m.download()
    with open(f, "r") as file:
        links = [line.strip() for line in file if line.strip()]

    await m.reply_text(f"Received {len(links)} links. Processing one by one...")

    for idx, url in enumerate(links, 1):
        try:
            await m.reply_text(f"Downloading video {idx}: {url}")
            # Quality choose - For simplicity, fixed 720p here, extend as needed
            quality = "720p"

            # Extract name from URL (simple)
            name = re.sub(r'\W+', '_', url)[:50]

            # Generate DRM player link for classplusapp DRM videos
            if "classplusapp.com/drm/" in url:
                video_id = url.split("/")[-1].split(".")[0]
                player_link = f"https://playerug.vercel.app/drm?video={video_id}"
                await m.reply_text(f"▶️ DRM Player Link:\n{player_link}")
                continue

            # Download video (placeholder)
            filename = await helper.download_video(url, f"{name}.mp4")
            caption = f"🎞️ Title: `{name} [{quality}]`\n🔗 Link: {url}\nExtracted by: {CREDIT}"

            await helper.send_vid(bot, m, caption, filename, None, name, None, m.chat.id)
        except Exception as e:
            await m.reply_text(f"Failed to download {url}\nError: {e}")

    os.remove(f)
    await m.reply_text("All links processed!")

if __name__ == "__main__":
    bot.start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))