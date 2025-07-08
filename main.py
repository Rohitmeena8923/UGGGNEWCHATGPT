import os
import re
import threading
import asyncio
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN, CREDIT
import helper

app = Flask(__name__)
bot = Client("telegram-drm-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.route("/")
def home():
    return "Bot is running!"

@bot.on_message(filters.command("start") & filters.private)
async def start_cmd(bot, m: Message):
    await m.reply_text(
        f"👋 Hello {m.from_user.first_name}!\n\n"
        f"📥 Send me a .txt file containing ClassPlus DRM links.\n"
        f"Use /help to see available commands."
    )

@bot.on_message(filters.command("help") & filters.private)
async def help_cmd(bot, m: Message):
    await m.reply_text(
        "**Available Commands:**\n"
        "/start - Start the bot\n"
        "/help - Show help\n"
        "/drmplayer - Get DRM player link from classplus video"
    )

@bot.on_message(filters.document & filters.private)
async def handle_txt_file(bot, m: Message):
    if not m.document.file_name.endswith(".txt"):
        return await m.reply_text("❌ Please upload a valid .txt file.")

    file_path = await m.download()
    with open(file_path, "r") as f:
        links = [line.strip() for line in f if line.strip()]

    await m.reply_text(f"✅ Received {len(links)} links.\nStarting processing...")

    for idx, url in enumerate(links, 1):
        try:
            await m.reply_text(f"📹 Processing video {idx}:\n{url}")
            if "classplusapp.com/drm/" in url:
                video_id = url.split("/")[-1].split(".")[0]
                drm_url = f"https://playerug.vercel.app/drm?video={video_id}"
                await m.reply_text(f"▶️ DRM Player Link:\n{drm_url}")
                continue

            name = re.sub(r'\W+', '_', url)[:50]
            filename = await helper.download_video(url, f"{name}.mp4")
            caption = f"🎞️ Title: `{name}`\n🔗 Link: {url}\n👤 Extracted by: {CREDIT}"
            await helper.send_vid(bot, m, caption, filename, None, name, None, m.chat.id)
        except Exception as e:
            await m.reply_text(f"⚠️ Failed to process: {url}\nError: `{e}`")

    os.remove(file_path)
    await m.reply_text("✅ All videos processed!")

def run_bot():
    bot.run()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))