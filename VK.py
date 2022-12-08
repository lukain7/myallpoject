import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from  vk_api.keyboard import VkKeyboard, VkKeyboardColor



vk_session = vk_api.VkApi(token = "794862088cc352943d2f2d8558d22591da84b17443229cd0574d15fa124a818f3476e7cfa6097b868056c")
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


def write_msg(id, text, keyboard = None):
    post = {"user_id" : id, "message" : text, "random_id" : 0}

    if keyboard != None:
        post["keyboard"] = keyboard.get_keyboard()
    else:
        post = post

    vk_session.method("messages.send", post)


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        msg = event.text.lower()
        id = event.user_id

        try:
            if msg in ["привет", "начать", "hi", "hello", "здравтсвуйте"]:
                keyboard = VkKeyboard()

                buttons = ["Команда","Help"]
                buttons_colors = [VkKeyboardColor.PRIMARY,  VkKeyboardColor.POSITIVE]
                for btn, btn_color in zip(buttons, buttons_colors):
                    keyboard.add_button(btn , btn_color)

                write_msg(id,"Добро пожаловать, вас приветствует команда ЛФК Адреналин.\n Здесь вы можете посмотреть состав команды, статистику игроков, ближайшие матчи\nКоманд",keyboard)


            elif msg == "команда":
                keyboard = VkKeyboard()

                buttons = ["Матчи", "Игроки", "Выход"]
                buttons_colors = [VkKeyboardColor.PRIMARY, VkKeyboardColor.POSITIVE, VkKeyboardColor.NEGATIVE]
                for btn, btn_color in zip(buttons, buttons_colors):
                    keyboard.add_button(btn, btn_color)

                write_msg(id, "Информация о команде", keyboard)
            elif msg == "выход":
                keyboard = VkKeyboard()

                buttons = ["Команда", "Help" ]
                buttons_colors = [VkKeyboardColor.PRIMARY, VkKeyboardColor.POSITIVE]
                for btn, btn_color in zip(buttons, buttons_colors):
                    keyboard.add_button(btn, btn_color)

                write_msg(id, "Начальное меню", keyboard)


            elif msg == "матчи":
                write_msg(id, "В ближайшее время матчей нет.")
            elif msg == "игроки":
                write_msg(id, "Капитан:\n Алексей Карасев\n Нападающие:\n 1. Магомед Мирзоев\n 2. Александр Дымов\n 3. Глеб Иванов\n 4. Шаха Хамидов\n Полузащитники:\n 1. Максим Шушунов\n 2.  Иван Лукьянов\n 3. Рубен Бабаян\n 4.Глеб Иванов \n Защитники:\n 1.Алексей Карасев\n 2. Михаил Веретнов\n 3. Роман Мотин\n 4. Глеб Иванов\n 5. Артем Миносян \n Вратари: \n 1.Вадим Губанов \n 2. Глеб Иванов \n")

            elif msg == "фото":
                write_msg(id, "Здесь в будут появляться фотографии с ближайших матчей.")


            elif msg == "help":
                 write_msg(id, "1)Привет\n Вызывает начальное меню\n2)Команда\n Вызывает меню - Информация о команде")

            elif msg == "атака":
                for i in range(1, 20):
                    write_msg(id, "ВОТ И ВСЕ")


            else:
                write_msg(id, "Иди учи алфавит, езжи да.\n Попробуй написать команду ПРИВЕТ!")

        except:
            pass