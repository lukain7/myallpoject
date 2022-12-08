import telebot
from telebot import types
import os
import gtts

token = "5191625849:AAEj27SksfLSV9rqsmHQk7YADvfNYTLEoj0"
bot = telebot.TeleBot(token)

def dlt():

    os.remove('tgvoice.mp3')

@bot.message_handler(commands=['start'])
def privet(message):
    if message.from_user.username == 'luka_7':
        bt = types.KeyboardButton('Записать голосовое')
        bt_1 = types.KeyboardButton('удалить ГС')
        fv = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(bt, bt_1)
        bot.send_message(message.chat.id, f"Здраствуйте, {message.from_user.first_name}!", reply_markup=fv)

    else:
        pass

@bot.message_handler(content_types=['text'])
def privet_1(message):

    if message.text.lower() == 'записать голосовое':

        msg = bot.send_message(message.chat.id, 'Напишите id, то кому будет отправлено голосовое:')
        bot.register_next_step_handler(msg, i_d)

    elif message.text.lower() == 'удалить ГС':

        dlt()

    else:
        pass
def i_d(message):

    global ID
    ID = int("{}".format(message.text))

    msg = bot.send_message(message.chat.id, 'Напищите текст для голосового сообщения:')
    bot.register_next_step_handler(msg, voice_1)

def voice_1(message):

    text = '{}'.format(message.text)
    spch = gtts.gTTS(text=text, lang='ru', slow=False)
    spch.save('anonim.mp3')
    f = open('anonim.mp3', 'rb')


    bot.send_audio(ID, f )
    privet(message)

bot.polling()