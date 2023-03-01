import telebot
import requests
import os
import shutil

from audio_transcription import get_large_audio_transcription
from summarization import summarize_text
from dotenv import load_dotenv

load_dotenv() 

TOKEN = os.getenv('API_SECRET')

bot = telebot.TeleBot(TOKEN)
isWaitingAudio = False

@bot.message_handler(commands=['start', 'resume' ,'help'])
def handle_message(message):
    print(message)
    global isWaitingAudio
    if message.text == '/start':
        bot.reply_to(message, "Por favor, envía un archivo de audio.")
        isWaitingAudio = True
    elif message.text == '/resume':
        bot.reply_to(message, "Por favor, envía el texto que deseas resumir.")
        bot.register_next_step_handler(message, summarize_message)
    elif message.text == '/help':
        bot.reply_to(message, "Comandos: \n 1.-/start : Iniciar bot \n 2.-/resume : Resumir texto")
    else:
        bot.reply_to(message, "Comando no válido.")

def summarize_message(message):
    print(message.text)
    try:
        summary = summarize_text(message.text)
        bot.reply_to(message,summary)
    except Exception as e:
        bot.reply_to(message, f"Ocurrió un error: {str(e)}")

@bot.message_handler(content_types=['audio', 'voice'])
def handle_audio(message):
    global isWaitingAudio
    try:
        if isWaitingAudio:
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
            shutil.rmtree('audio-chunks')
            isWaitingAudio = False
    except Exception as e:
        bot.reply_to(message, f"Ocurrió un error: {str(e)}")

bot.polling()