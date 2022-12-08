import telebot
from telebot import types
import sqlite3
import time

# токен noname bot
token = '5191625849:AAEj27SksfLSV9rqsmHQk7YADvfNYTLEoj0'

#токен shop bot
#token_1 = '5560336361:AAGspd6eaxuBh3Nr1kBMlPtXAiiAZy5TnWc'
bot = telebot.TeleBot(token)


# начальное меню
@bot.message_handler(commands = ['start'])
def privet(message):

    status = ['creator', 'administrator']
    if bot.get_chat_member(message.chat.id, message.from_user.id).status in status:

        bt1 = types.KeyboardButton('info')
        bt2 = types.KeyboardButton('delete people')
        klava = types.ReplyKeyboardMarkup(resize_keyboard=True).row(bt1, bt2)
        bot.send_message(message.chat.id, 'Добро пожаловать, СЭР!', reply_markup=klava)
    
    else:

        global sql
        global c

        sql = sqlite3.connect('market.db')
        c = sql.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS purchase(
                id INT,
                name TEXT,
                username TEXT,
                phone TEXT
        )""")
        sql.commit()
        user = [message.from_user.id, message.from_user.first_name, message.from_user.username, None]
        c.execute(f"SELECT name FROM purchase WHERE id={message.from_user.id}")
        if c.fetchone() is None:
            c.execute("INSERT INTO purchase VALUES(?, ?, ?, ?);", user)
            sql.commit()
        else:
            pass

        bt1  = types.KeyboardButton('📞')
        bt2 =  types.KeyboardButton('💸Сделать заказ💸')
        klava = types.ReplyKeyboardMarkup(resize_keyboard=True).row(bt1, bt2) # ---> Встроку

        bot.send_message(message.chat.id, f"Добро пожаловать, <i>{message.from_user.first_name}</i>", parse_mode="html", reply_markup=klava)
    """Получаем информацию о пользователе, 
        который нажал команду /start."""

# бот получает текстовые сообщения
@bot.message_handler(content_types = ['text'])
def otvet(message):

    

    if message.text.lower() in ['здравствуйте','привет','hello','добрый день','добрый вечер', 'hi']:
        bot.send_message(message.chat.id, f'{message.from_user.first_name}\nВы хотите сделать заказ?')

    elif message.text == '📞':
        msg = bot.send_message(message.chat.id, 'Введите свой номер:\nСвами свяжется наш менеджер!')
        bot.register_next_step_handler(msg, phone)

    elif message.text == '💸Сделать заказ💸':


        b1 = types.KeyboardButton('Vetements')
        b2 = types.KeyboardButton('Essentials')
        b3 = types.KeyboardButton('Jordan')
        b4 = types.KeyboardButton('🛒Back🛒')


        kv = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(b1, b2, b3, b4)
        asd = bot.send_message(message.chat.id, '-Товары-\nКакой товар вас интересует?', reply_markup=kv)
        bot.register_next_step_handler(asd , purchase)

    elif message.text.lower() == 'info':
        f = open('market.db', 'rb')
        bot.send_document(message.chat.id, f)
        
    elif message.text.lower() == 'delete people':
        
        s = bot.send_message(message.chat.id, "Введите id пользователя, которого вы хотели удалить:")
        bot.register_next_step_handler(s, delt)

    else:
        pass

# пользоваьель получает чек
def chek(message):
    global ID
    ID  = 877008114
    if message.from_user.username == None:

            bot.send_message(message.chat.id, 'Оставьте свой телефон для дальнейшей связи!')

            y1 = types.KeyboardButton('📞')

            y = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(y1)

            bot.send_message(message.chat.id, 'Нажмите на кнопку клавиатуры, чтобы оставить номер.', reply_markup=y)
            
    else:
        bot.send_message(ID, "Был оформлен заказ!")
        back(message)

# удаление пользователя для администратора
def delt(message):

    a = '{}'.format(message.text)
    sql = sqlite3.connect('market.db')
    c = sql.cursor()

    c.execute(f"DELETE FROM purchase WHERE id = {a}")
    sql.commit()
    bot.send_message(message.chat.id, "Пользователь удален!")
    bot.register_next_step_handler(back)

# возвращение домой, на начальное меню
def back(message):

    bt1 = types.KeyboardButton('📞')
    bt2 = types.KeyboardButton('💸Сделать заказ💸')

    klava = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(bt1, bt2)

    bot.send_message(message.chat.id, 'Спасибо за заказ!\nПриходите  ещё!', reply_markup=klava)

# пользователь получает телефон пользователя
def phone(message):

    sql = sqlite3.connect('market.db')
    c = sql.cursor()

    a = "{}".format(message.text)
    
    c.execute(f"UPDATE purchase SET phone = {a} WHERE id = {message.from_user.id};")
    sql.commit()
    print('Номер пользователя добавлен!')
    bot.send_message(message.chat.id, f'{message.from_user.first_name}, ваш номер записан!\n С вами свяжется наш менеджер.')

    back(message)

# бот проверяет фирма одежды это или что-то другое
def purchase(message):

    if message.text.lower() in ['vetements', 'essentials', 'jordan']:

        global vech
        a = "{}".format(message.text)
        vech = a
       
        t1 = types.KeyboardButton('S')
        t2 = types.KeyboardButton('M')
        t3 = types.KeyboardButton('L')
        t4 = types.KeyboardButton('XL')
        t5 = types.KeyboardButton('🛒Back🛒')

        sz = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(t1, t2, t3, t4)
        sz.add(t5)

        ms = bot.send_message(message.chat.id, f'<i>{message.from_user.first_name}</i>, какой размер?', reply_markup=sz,
                                  parse_mode='html')
        bot.register_next_step_handler(ms, size)

    elif message.text == '🛒Back🛒':
        back(message)

    else:
        pass

# бот проверяет размер одежды это или что-то другое
def size(message):

    if message.text in ['S', 'M', 'L', 'XL' ]:
        global razmer

        a = "{}".format(message.text)
        razmer = a

        s = bot.send_message(message.chat.id, "Введите количество вещей:")
        bot.register_next_step_handler(s, kol)

    elif message.text == '🛒Back🛒':
 
        back(message)

    else:
        pass

# бот получает  количество вещей, которые пользователь хочет заказать
def kol(message):
    
    global local_date
    global umnoj

    a = "{}".format(message.text)
    umnoj = int(a)
  
    seconds = time.time()
    local_date = time.ctime(seconds)
    
    if vech == "Vetements":
        sum_1 = 4990
        sum_1 = sum_1 * umnoj
        ID  = 877008114

        bot.send_message(message.chat.id, f"<b>ЧЕК</b>\n<i>Покупатель:</i> <b>{message.from_user.first_name}</b>\n <i>СУММА</i> - {sum_1}\nвещь - {vech}\nразмер - {razmer}\nколичество - {a}\nвремя покупки - {local_date} ", parse_mode="html")
        bot.send_message(ID, f"<b>ЧЕК</b>\n<i>Покупатель:</i> <b>{message.from_user.first_name}</b>\nid - {message.from_user.id}\n <i>СУММА</i> - {sum_1}\nвещь - {vech}\nразмер - {razmer}\nколичество - {a}\nвремя покупки - {local_date} ", parse_mode="html")
        chek(message)

    elif vech == "Essentials":
        sum_1 = 4490
        sum_1 = sum_1 * umnoj
        ID  = 877008114

        bot.send_message(message.chat.id, f"<b>ЧЕК</b>\n<i>Покупатель:</i> <b>{message.from_user.first_name}</b>\n <i>СУММА</i> - {sum_1}\nвещь - {vech}\nразмер - {razmer}\nколичество - {a}\nвремя покупки - {local_date} ", parse_mode="html")
        bot.send_message(ID, f"<b>ЧЕК</b>\n<i>Покупатель:</i> <b>{message.from_user.first_name}</b>\nid - {message.from_user.id}\n <i>СУММА</i> - {sum_1}\nвещь - {vech}\nразмер - {razmer}\nколичество - {a}\nвремя покупки - {local_date} ", parse_mode="html")
        chek(message)

    elif vech == "Jordan":
        sum_1 = 2290
        sum_1 = sum_1 * umnoj
        ID  = 877008114

        bot.send_message(message.chat.id, f"<b>ЧЕК</b>\n<i>Покупатель:</i> <b>{message.from_user.first_name}</b>\n <i>СУММА</i> - {sum_1}\nвещь - {vech}\nразмер - {razmer}\nколичество - {a}\nвремя покупки - {local_date} ", parse_mode="html")
        bot.send_message(ID, f"<b>ЧЕК</b>\n<i>Покупатель:</i> <b>{message.from_user.first_name}</b>\nid - {message.from_user.id}\n <i>СУММА</i> - {sum_1}\nвещь - {vech}\nразмер - {razmer}\nколичество - {a}\nвремя покупки - {local_date} ", parse_mode="html")
        chek(message)

    else:
        pass


if __name__ == '__main__':
    bot.polling()