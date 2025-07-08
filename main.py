import re
import asyncio
import os
import threading
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
    await m.reply_text(
        f"👋 Hello {m.from_user.first_name}!\n\n"
        "Send me a `.txt` file with ClassPlus DRM video links.\n\n"
        "Use /help to see all commands."
    )

@bot.on_message(filters.command("help") & filters.private)
async def help_cmd(bot, m: Message):
    help_text = """
<b>📌 Available Commands:</b>

/start - Start the bot
/help - Show this help menu
/drmplayer - Get DRM player link from ClassPlus DRM URL

Just send a .txt file with links to begin downloading!
"""
    await m.reply_text(help_text)

@bot.on_message(filters.document & filters.private)
async def doc_handler(bot, m: Message):
    if not m.document.file_name.endswith(".txt"):
        await m.reply_text("❌ Please send a valid `.txt` file containing video links.")
        return

    f = await m.download()
    with open(f, "r") as file:
        links = [line.strip() for line in file if line.strip()]

    await m.reply_text(f"✅ Received {len(links)} links. Starting download one by one...")

    for idx, url in enumerate(links, 1):
        try:
            await m.reply_text(f"🔽 Processing link {idx}:\n{url}")

            # Quality input (default 720p for now)
            quality = "720p"

            # Simple filename from URL
            name = re.sub(r'\W+', '_', url)[:50]

            # Generate DRM player link
            if "classplusapp.com/drm/" in url:
                video_id = url.split("/")[-1].split(".")[0]
                player_link = f"https://playerug.vercel.app/drm?video={video_id}"
                await m.reply_text(f"▶️ DRM Player Link:\n{player_link}")
                continue

            # Download video (You can customize quality, thumbnail, etc.)
            filename = await helper.download_video(url, f"{name}.mp4")
            caption = f"🎞️ Title: `{name} [{quality}]`\n🔗 Link: {url}\n👤 Extracted by: `{CREDIT}`"

            await helper.send_vid(bot, m, caption, filename, None, name, None, m.chat.id)

        except Exception as e:
            await m.reply_text(f"❌ Failed to download {url}\n\nError: {e}")

    os.remove(f)
    await m.reply_text("✅ All links processed successfully!")

# Run bot and Flask server together
if __name__ == "__main__":
    def run_bot():
        bot.run()

    threading.Thread(target=run_bot).start()

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))