import telebot
import time
from telebot import types
import os


bot = telebot.TeleBot('6748343854:AAG0G4lj8aNIwvk66A9YR-f1F6x_0pxwtcY')

kick_tf = False
mute_tf = False
spam_tf = False
delete_user_command = ""
mute_user_command = ""
mute_time = 0
user_token = ""
fuser_token = ""
chat_id = ''


@bot.message_handler(commands=['start'])
def startBot(message):
    first_mess = f"<b>{message.from_user.first_name} </b>, привет!\nХочешь создать бота?"
    markup = types.InlineKeyboardMarkup()
    button_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    markup.add(button_yes)
    bot.send_message(message.chat.id, first_mess, parse_mode='html',
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def response(function_call):
    if function_call.message:
        if function_call.data == "yes":
            second_mess = "Зайди в мессенджер @BotFather и зарегистрируй там имя своего бота, после тебе там же скинут уникальный токен, присылай его сюда!"
            sent = bot.send_message(function_call.message.chat.id, second_mess)
            bot.register_next_step_handler(sent, save_token)
            bot.answer_callback_query(function_call.id)
    bot.answer_callback_query(function_call.id)


def save_token(message):
    global user_token, fuser_token
    user_token = message.text
    fuser_token = user_token.replace(":", "_")
    bot.send_message(message.chat.id, f'Ваш токен: {user_token}')
    bot.send_message(message.chat.id,
                     text="Хорошо, {0.first_name}! Теперь выбери функции, которые хочешь добавить в своего бота!".format(
                         message.from_user))
    vibor(message)


def vibor(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                       one_time_keyboard=True)
    btn1 = types.KeyboardButton("❌ Удаление пользователя из канала")
    btn2 = types.KeyboardButton("🔇 Заглушение пользователя на время")
    btn3 = types.KeyboardButton("🤬 Защита от спама и сквернословия")
    btn4 = types.KeyboardButton("✅ Завершить создание бота")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, "Функции:", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def act_li(message):
    if message.text == "❌ Удаление пользователя из канала":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                           one_time_keyboard=True)
        btn1 = types.KeyboardButton("Да")
        btn2 = types.KeyboardButton("Нет")
        markup.add(btn1, btn2)
        msg = bot.send_message(message.chat.id,
                               "Вы хотите иметь функцию удаления пользователя из канала?",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, process_delete_user_step)

    elif message.text == "🔇 Заглушение пользователя на время":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                           one_time_keyboard=True)
        btn1 = types.KeyboardButton("Да")
        btn2 = types.KeyboardButton("Нет")
        markup.add(btn1, btn2)
        msg = bot.send_message(message.chat.id,
                               "Вы хотите иметь функцию заглушения пользователя на время?",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, process_mute_user_step)

    elif message.text == "🤬 Защита от спама и сквернословия":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                           one_time_keyboard=True)
        btn1 = types.KeyboardButton("Да")
        btn2 = types.KeyboardButton("Нет")
        markup.add(btn1, btn2)
        msg = bot.send_message(message.chat.id,
                               "Вы хотите иметь функцию фильтрации слов?",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, process_def_user_step)

    elif message.text == "✅ Завершить создание бота":
        bot.send_message(message.chat.id, text="Ваш бот создан")
        global chat_id
        chat_id = message.chat.id
        return proga(kick_tf, mute_tf, spam_tf, spisok, delete_user_command, mute_user_command, mute_time, user_token, chat_id)

    else:
        bot.send_message(message.chat.id,
                         text="На такую комманду я не запрограммирован..")


def process_delete_user_step(message):
    global kick_tf
    if (message.text == "Да"):
        kick_tf = True
        msg = bot.send_message(message.chat.id,
                               "Какой командой будет проводиться удаление пользователя(на английском языке)? (по умолчанию 'kick')")
        bot.register_next_step_handler(msg, save_delete_user_command)
    else:
        kick_tf = False
        bot.send_message(message.chat.id, "Выберите другую функцию.")
        vibor(message)


def save_delete_user_command(message):
    global delete_user_command
    delete_user_command = message.text
    bot.send_message(message.chat.id,
                     f'Команда для удаления пользователя: {delete_user_command}. Учтите, что администраторов нельзя выгонять!')
    vibor(message)


def process_mute_user_step(message):
    global mute_tf
    if (message.text == "Да"):
        mute_tf = True
        msg = bot.send_message(message.chat.id,
                               "Какой командой будет проводиться заглушение пользователя(на английском языке)? Учтите, что отмена заглушения будет проводится командой с добавлением un (по умолчанию 'mute' и 'unmute')")
        bot.register_next_step_handler(msg, save_mute_user_command)
    else:
        mute_tf = False
        bot.send_message(message.chat.id, "Выберите другую функцию.")
        vibor(message)


def process2_time(message):
    global mute_time
    mute_time = int(message.text)
    bot.send_message(message.chat.id, f'Время: {mute_time} минут')
    vibor(message)


def save_mute_user_command(message):
    global mute_user_command
    mute_user_command = message.text
    bot.send_message(message.chat.id,
                     f'Команда для удаления пользователя: {mute_user_command}')
    msg = bot.send_message(message.chat.id,
                           "Сколько времени будет длиться заглушение?")
    bot.register_next_step_handler(msg, process2_time)


def process_def_user_step(message):
    global spam_tf
    if (message.text == "Да"):
        spam_tf = True
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                           one_time_keyboard=True)
        btn1 = types.KeyboardButton("Хватит")
        markup.add(btn1)
        msg = bot.send_message(message.chat.id,
                               "Напишите, за какие слова пользователь будет блокироваться. Когда закончите, нажмите кнопку 'Хватит'",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, spisok_slov)
    else:
        spam_tf = False
        bot.send_message(message.chat.id, "Выберите другую функцию.")
        vibor(message)


spisok = list()


def spisok_slov(message):
    if (message.text == "Хватит"):
        bot.send_message(message.chat.id, "Выберите другую функцию.")
        vibor(message)
    else:
        msg = message.text
        spisok.append(msg)
        msg1 = bot.send_message(message.chat.id, "Слово добавлено, далее.")
        bot.register_next_step_handler(msg1, spisok_slov)

def proga(*args):
    global kick_tf, mute_tf, spam_tf, chat_id
    with open(f'{fuser_token}.py', 'w+', encoding='utf-8') as file:
        file.write(f"import telebot\nimport time\nbot ="
                   f" telebot.TeleBot('{user_token}')\n\n@bot.message_handler"
                   f"(commands=['start'])\ndef start(message):\n  bot.reply_to"
                   f"(message, 'Привет! Я бот для управления чатом. Напиши "
                   f"/help, чтобы узнать, что я умею.')\n\n")
        if kick_tf or mute_tf:
            file.write(f"@bot.message_handler(commands=['help'])\n"
                       f"def help(message):\n    bot.reply_to(message,' ")
            if kick_tf:
                file.write(f"/{delete_user_command} - кикнуть пользователя\\n")
            if mute_tf:
                file.write(
                    f"/{mute_user_command} - замутить пользователя на {mute_time} минут\\n/un{mute_user_command} - размутить пользователя")
            file.write("')\n")
        if kick_tf:
            file.write(f"@bot.message_handler(commands=['{delete_user_command}'])\n"
                       f"def kick_user(message):\n    if message.reply_to_message:\n"
                       f"        user_id = message.reply_to_message.from_user.id\n        chat_id = message.chat.id\n" 
                       f"        user_status = bot.get_chat_member(chat_id, user_id).status\n"
                       f"        if (user_status"
                       f" == 'administrator') or (user_status == 'creator'):\n"
                       f"            bot.reply_to(message, 'Невозможно кикнуть администратора.')\n"
                       f"        else:\n            bot.kick_chat_member(chat_id, user_id)\n"
                       f"            bot.reply_to(message, f'Пользователь {{message.reply_to_message.from_user.username}} был удален.')\n"
                       f"    else:\n"
                       f"        bot.reply_to(message, 'Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите кикнуть.')\n")
        if mute_tf == True:
            file.write(f"@bot.message_handler(commands=['{mute_user_command}'])\ndef mute_user(message):\n    if message.reply_to_message:\n"
                       f"        chat_id = message.chat.id\n        user_id = message.reply_to_message.from_user.id\n"
                       f"        user_status = bot.get_chat_member(chat_id, user_id).status\n        if (user_status == 'administrator') or (user_status == 'creator'):\n"
                       f"            bot.reply_to(message, 'Невозможно замутить администратора.')\n        else:\n"
                       f"            duration = {mute_time}\n            bot.restrict_chat_member(chat_id, user_id, until_date=time.time()+duration*60)\n"
                       f"            bot.reply_to(message, f'Пользователь {{message.reply_to_message.from_user.username}} замучен на {{duration}} минут.')\n    else:\n"
                       f"        bot.reply_to(message, 'Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите замутить.')"
                       f"@bot.message_handler(commands=['un{mute_user_command}'])\ndef unmute_user(message):\n    if message.reply_to_message:\n"
                       f"        chat_id = message.chat.id\n        user_id = message.reply_to_message.from_user.id\n"
                       f"        bot.restrict_chat_member(chat_id, user_id, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True)\n"
                       f"        bot.reply_to(message, f'Пользователь {{message.reply_to_message.from_user.username}} размучен.')\n    else:\n"
                       f"        bot.reply_to(message, 'Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите размутить.')\n\n")
        if spam_tf == True:
            file.write(f"bad_words = {spisok}\n"
                       f"def check_message(message):\n    for word in bad_words:\n        if word in message.text.lower():\n"
                       f"            return True\n    return False\n\n"
                       f"@bot.message_handler(func=lambda message: True)\ndef handle_message(message):\n"
                       f"    if check_message(message):\n        bot.kick_chat_member(message.chat.id, message.from_user.id)\n"
                       f"        bot.send_message(message.chat.id, f'Пользователь {{message.from_user.username}} был удален из чата за использование запрещенных слов')\n"
                       f"    else:\n        print(message.text)\n\n")
        file.write('bot.infinity_polling(none_stop=True)')
        file.seek(0)
        bot.send_document(chat_id=chat_id, document=file)
    os.system(f'python {fuser_token}.py')
    kick_tf = False
    mute_tf = False
    spam_tf = False






bot.infinity_polling(none_stop=True)
