import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
import datetime
import wikipedia
wikipedia.set_lang("RU")
import requests
from bs4 import BeautifulSoup
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import json
from random import randint

# хост бота, вставляем ключ API
vk_session = vk_api.VkApi(token="794862088cc352943d2f2d8558d22591da84b17443229cd0574d15fa124a818f3476e7cfa6097b868056c")
longpool = VkBotLongPoll(vk_session, 205902912)
vk = vk_session.get_api()

# функция отправки сообщения
def send(id, text):
    vk_session.method("messages.send", {'chat_id' : id, "message" : text, "random_id" : 0 })

# функция отправки сообщения с клавиатурой
def sender(id, text, keyboard_c):
    vk_session.method("messages.send", {'chat_id' : id, "message" : text,"keyboard": keyboard_c, "random_id" : 0 })

# общая функция
def main():

    # создаем клавитуру
    keyboard_1 = VkKeyboard(one_time=False, inline=True)
    keyboard_1.add_callback_button(label='Темы Докладов', color=VkKeyboardColor.SECONDARY, payload={'type' : 'open_link', 'link' : 'https://vk.com/away.php?to=https%3A%2F%2Fdrive.google.com%2Fdrive%2Ffolders%2F1jl7BwOVqRqi8vXVa3RemRTTrcqx6RmO-&cc_key='})
    keyboard_1.add_line()
    keyboard_1.add_callback_button(label='Учебные материалы', color=VkKeyboardColor.SECONDARY, payload={'type' : 'open_link', 'link' : 'https://vk.com/away.php?utf=1&to=https%3A%2F%2Fdrive.google.com%2Fdrive%2Ffolders%2F1tmv7VsPyP2z1XZNDgb35Iu8yIHjGi7Wz'})


    for event in longpool.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:

            id = event.chat_id
            msg = event.object.message['text'].lower()
            
            # проверка на нвого пользователя группы
            try:
                dey = event.message.action['type']
                invite_id = event.message.action['member_id']
            except:
                dey = ''
                invite_id = -100

            try:
                # если новый пользователь, то бот его приветствует
                if dey == 'chat_invite_user':
                    send(id, f"Добро пожаловать в нашу группу, @id{invite_id}\nпропробуй команду  - help.")

                # узнаем сколько времени
                elif msg in ["время", "1"]:

                    send(id, "Московское время: " + str(datetime.datetime.today().strftime("%H : %M")))
                # узнаем погоду(температуру)
                elif msg in ["погода" , "2"]:

                    url = "https://world-weather.ru/pogoda/russia/moscow/"
                    response = requests.get(url)
                    bs = BeautifulSoup(response.text, "lxml")

                    day_week =  bs.find('div', class_="day-week").text
                    day = bs.find('div', class_="numbers-month").text
                    month = bs.find('div', class_="month").text
                    temp_1 = bs.find('div', class_="day-temperature").text
                    temp_2 = bs.find('div', class_="night-temperature").text
                    send(id, f'Погода\n{day_week}\n{day} {month}\n днем:  {temp_1}\n ночью: {temp_2}')

                #отправляем ответ на запрос из wikipedia
                elif msg in ["википедия", "вики", "wikipedia", "wiki", "3"]:
                    send(id, "Введите запрос: ")
                    for event in longpool.listen():
                        if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
                            send(id, "Вот что я нашел: \n" + str(wikipedia.summary(event.object.message['text']))) 
                            break

                # отпрвляем ссылки на доп.материалы, таблицы
                elif msg in ["документы", "доки", "4"]:
                    sender(id, "Ссылки", keyboard_c=keyboard_1.get_keyboard())

                elif msg in ['команды', 'команд', 'помощь', "help", "5"]:
                    send(id, """Команды\n1 - время\n    прислыет время на данный момент\n2 - погода\n    присылает погоду на данный момент\n3 - википедия\n    присылает ответна введенный вами запрос\n4 - документы\n    отправляет ссылки на таблицы домашних заданий и  учебные материалы\n5 - help\n    вызывает данное меню\n6 - анекдот""")
                                    
                elif msg in ['анекдот', 'анек', '6']:
                    url_1 = "https://anekdotbar.ru/top-100.html"
                    res = requests.get(url_1)
                    soup = BeautifulSoup(res.text, "lxml")

                    anekd = soup.find_all('div', class_="tecst")
                    A = []
                    for i in anekd:
                        A.append(i.text)
                    a = randint(0, 99)
                    send(id, A[a])

                elif msg in ['рулетка', '7']:
                    A = ['Кирилл', 'Женя', 'Иван', 'Ксения', 'Егор', 'Дмитрий', 'Алена', 'Даниил', 'Полина']
                    B = ['Кириллу', 'Жене', 'Ивану', 'Ксении', 'Егору', 'Дмитрию', 'Алене', 'Даниилу', 'Полине']
                    s = randint(0, 8)
                    f = randint(0, 1)
                    if f == 0:
                        send(id, f"Выстрел...\nПромах, {B[s]}, повезло")
                    else:
                        send(id, f"Выстрел...\n{A[s]} был(а) убит(а)...")

                else:
                    pass
            except AttributeError:
                pass

        # для обработки действия callback-копки
        elif event.type == VkBotEventType.MESSAGE_EVENT:
            if event.object.payload.get("type") == "open_link":
                vk.messages.sendMessageEventAnswer(event_id= event.object.event_id, user_id=event.object.user_id, peer_id=event.object.peer_id ,event_data = json.dumps(event.object.payload))


if __name__ == "__main__":
    main()