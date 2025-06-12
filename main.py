
from pyrogram import Client, filters
import yt_dlp
import os
import re

API_ID = 22134277
API_HASH = "3a51c589b4e41d7f8e4d0d756fb94665"
BOT_TOKEN = "7566323819:AAFWjLXaiP921wwHWJaeI-CaCzHxWu6XQZM"

app = Client("video_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("👋 أهلاً بك في بوت تحميل الفيديوهات.\n\nأرسل رابط من YouTube أو TikTok أو Instagram لتحميله.")

@app.on_message(filters.text & ~filters.command("start"))
async def download_video(client, message):
    url = message.text.strip()

    if not url.startswith("http") or not re.search(r"(youtube\.com|youtu\.be|tiktok\.com|instagram\.com)", url, re.IGNORECASE):
        return await message.reply("⚠️ الرابط غير مدعوم! فقط YouTube أو TikTok أو Instagram")

    msg = await message.reply("⏳ جاري التحميل...")

    try:
        ydl_opts = {
            "outtmpl": "%(title)s.%(ext)s",
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
            "merge_output_format": "mp4",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)

        await msg.edit("📤 جاري رفع الفيديو...")
        await client.send_video(chat_id=message.chat.id, video=file_name, caption="✅ تم التحميل بنجاح")
        os.remove(file_name)

    except Exception as e:
        await msg.edit(f"❌ حدث خطأ: {str(e)}")

app.run()
