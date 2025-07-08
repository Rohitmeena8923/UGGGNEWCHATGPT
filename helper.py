import aiohttp
import aiofiles
import os
from pyrogram import Client

# Async video downloader placeholder
async def download_video(url: str, filename: str) -> str:
    """
    Simple async downloader using aiohttp.
    Saves video from url to filename.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    raise Exception(f"Failed to download file: HTTP {resp.status}")
                f = await aiofiles.open(filename, mode='wb')
                await f.write(await resp.read())
                await f.close()
        return filename
    except Exception as e:
        raise e

async def send_vid(bot: Client, m, caption: str, filename: str, thumb, name, prog, chat_id: int):
    """
    Sends video to chat_id with caption.
    """
    try:
        await bot.send_video(
            chat_id,
            video=filename,
            caption=caption,
            supports_streaming=True,
            # thumbnail=thumb  # optional if you implement thumbnail upload
        )
    except Exception as e:
        await bot.send_message(chat_id, f"Error sending video: {e}")
    finally:
        if os.path.exists(filename):
            os.remove(filename)