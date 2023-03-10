import telebot
import requests
import os
import shutil

from audio_transcription import get_large_audio_transcription
from summarization import summarize_text
from dotenv import load_dotenv
from normal_summary import generate_summarize
from image_to_text import convert_to_text

load_dotenv() 

TOKEN = os.getenv('API_SECRET')

bot = telebot.TeleBot(TOKEN)
isWaitingAudio = False

@bot.message_handler(commands=['audio', 'resumenai' ,'help', 'resumen', 'photo'])
def handle_message(message):
    global isWaitingAudio
    if message.text == '/audio':
        bot.reply_to(message, "Por favor, envía un archivo de audio.")
        isWaitingAudio = True
    elif message.text == '/resumenai':
        bot.reply_to(message, "Por favor, envía el texto que deseas resumir.")
        bot.register_next_step_handler(message, summarize_message_ai)
    elif message.text == '/help':
        bot.reply_to(message, "Comandos: \n 1.-/audio : Mandar audio para realizar un resumen \n 2.-/resumenai : Resumir texto (A.I) \n 3.-/resumen : Resumis texto (Spacy)")
    elif message.text == '/resumen':
        bot.reply_to(message, "Por favor, envía el texto que deseas resumir.")
        bot.register_next_step_handler(message, summarize_message)
    else:
        bot.reply_to(message, "Comando no válido.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    text = convert_to_text(downloaded_file)
    bot.reply_to(message, text)

def summarize_message_ai(message):
    try:
        summary = summarize_text(message.text)
        bot.reply_to(message,summary)
    except Exception as e:
        bot.reply_to(message, f"Ocurrió un error: {str(e)}")

def summarize_message(message):
    try:
        summary = generate_summarize(message.text,3)
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

@bot.message_handler(commands=['start'])
def handle_menu(message):
    menu_markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    button1 = telebot.types.InlineKeyboardButton(text='Ayuda', callback_data='option1')
    button2 = telebot.types.InlineKeyboardButton(text='Resumir Audio (I.A)', callback_data='option2')
    button3 = telebot.types.InlineKeyboardButton(text='Resumir Texto (I.A)', callback_data='option3')
    button4 = telebot.types.InlineKeyboardButton(text='Resumir Texto (Spacy)', callback_data='option4')
    menu_markup.add(button1, button2, button3, button4)
    bot.send_message(message.chat.id, 'Selecciona una opción:', reply_markup=menu_markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    global isWaitingAudio
    if call.data == 'option1':
        bot.send_message(call.message.chat.id, 'Comandos: \n 1.-/audio : Mandar audio para realizar un resumen \n 2.-/resumenai : Resumir texto (A.I) \n 3.-/resumen : Resumis texto (Spacy)')
    elif call.data == 'option2':
        bot.send_message(call.message.chat.id, 'Por favor, envía un archivo de audio.')
        isWaitingAudio = True
    elif call.data == 'option3':
        bot.send_message(call.message.chat.id, 'Por favor, envía el texto que deseas resumir.')
        bot.register_next_step_handler(call.message, summarize_message_ai)
    elif call.data == 'option4':
        bot.send_message(call.message.chat.id, 'Por favor, envía el texto que deseas resumir.')
        bot.register_next_step_handler(call.message, summarize_message)

bot.polling()