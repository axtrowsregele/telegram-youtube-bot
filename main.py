import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import yt_dlp

TOKEN = os.environ['BOT_TOKEN']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Trimite un link YouTube cu /play [link]")

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Trimite un link cu /play [link]")
        return
    url = context.args[0]
    await update.message.reply_text("Se descarcă...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'song.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    await update.message.reply_audio(audio=open("song.mp3", "rb"))

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("play", play))

app.run_polling()
