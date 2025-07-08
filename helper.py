async def download_video(url, output_name):
    import aiofiles
    async with aiofiles.open(output_name, 'w') as f:
        await f.write("dummy")  # Placeholder logic
    return output_name

async def send_vid(bot, m, caption, filename, thumb, name, prog, channel_id):
    await m.reply_document(filename, caption=caption)