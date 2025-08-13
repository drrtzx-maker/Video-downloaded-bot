import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل رابط الفيديو وسأحمله لك 📥")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    await update.message.reply_text("جارِ التحميل، انتظر لحظة ⏳...")

    try:
        ydl_opts = {
            'outtmpl': 'video.%(ext)s',
            'format': 'best',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # إرسال الفيديو
        for file in os.listdir():
            if file.startswith("video"):
                await update.message.reply_video(video=open(file, "rb"))
                os.remove(file)
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ: {e}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

app.run_polling()
