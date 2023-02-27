import telebot
import requests
import os
from audio_transcription import get_large_audio_transcription
from summarization import summarize_text
from dotenv import load_dotenv

load_dotenv() 

TOKEN = os.getenv('API_SECRET')

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Por favor, envía un archivo de audio.")

@bot.message_handler(content_types=['audio', 'voice'])
def handle_audio(message):
    print('AUDIO????')
    try:
        bot.reply_to(message, "Procesando...")
        if message.audio:
            file_info = bot.get_file(message.audio.file_id)
        elif message.voice:
            file_info = bot.get_file(message.voice.file_id)
        else:
            bot.reply_to(message, "Solo se permiten archivos de audio en formato mp3")
            return
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path))
        with open('audio.mp3', 'wb') as f:
            f.write(file.content)
        text = get_large_audio_transcription('audio.mp3')
        summary = summarize_text(text)
        bot.reply_to(message, summary)
        os.remove('audio.mp3')
    except Exception as e:
        bot.reply_to(message, f"Ocurrió un error: {str(e)}")

bot.polling()