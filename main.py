from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from youtubesearchpython import VideosSearch
import os
import yt_dlp

TOKEN = "8168060031:AAGRRGLXzs7ICqfwgnlrZU5ZgUr-_uwdSBY"

def download_song(query):
    search = VideosSearch(query, limit=1)
    result = search.result()['result'][0]
    video_link = result['link']
    title = result['title']

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f"{title}.mp3",
        'quiet': True,
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_link])

    return title, video_link

def start(update, context):
    update.message.reply_text("🎵 Merhaba! Şarkı ismini ve sanatçı adını yaz, hemen bulayım!")

def search_and_send(update, context):
    query = update.message.text
    msg = update.message.reply_text(f"🔍 '{query}' aranıyor...")

    try:
        title, video_link = download_song(query)
        audio_file = f"{title}.mp3"

        with open(audio_file, 'rb') as audio:
            update.message.reply_audio(audio, title=title)

        update.message.reply_text(f"✅ Şarkıyı indir: [İndir]({video_link})", parse_mode='Markdown')

        os.remove(audio_file)

        msg.delete()

    except Exception as e:
        msg.edit_text(f"Hata oluştu: {e}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, search_and_send))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
