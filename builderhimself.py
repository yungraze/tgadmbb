import telebot
import time
from telebot import types


bot = telebot.TeleBot('6748343854:AAG0G4lj8aNIwvk66A9YR-f1F6x_0pxwtcY')



@bot.message_handler(commands=['start'])
def startBot(message):
    first_mess = f"<b>{message.from_user.first_name} </b>, привет!\nХочешь создать бота?"
    markup = types.InlineKeyboardMarkup()
    button_yes = types.InlineKeyboardButton(text = 'Да', callback_data='yes')
    markup.add(button_yes)
    bot.send_message(message.chat.id, first_mess, parse_mode='html', reply_markup=markup)

@bot.callback_query_handler(func=lambda call:True)
def response(function_call):
  if function_call.message:
     if function_call.data == "yes":
        second_mess = "Зайди в мессенджер @BotFather и зарегистрируй там имя своего бота, после тебе там же скинут уникальный токен, присылай его сюда!"
        sent = bot.send_message(function_call.message.chat.id, second_mess)
        bot.register_next_step_handler(sent, save_token)
        bot.answer_callback_query(function_call.id)
  bot.answer_callback_query(function_call.id)


def save_token(message):
    user_token = message.text
    bot.send_message(message.chat.id, f'Ваш токен: {user_token}')
    bot.send_message(message.chat.id,text="Хорошо, {0.first_name}! Теперь выбери функции, которые хочешь добавить в своего бота!".format(message.from_user))
    vibor(message)

def vibor(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton("❌ Удаление пользователя из канала")
    btn2 = types.KeyboardButton("🔇 Заглушение пользователя на время")
    btn3 = types.KeyboardButton("🤬 Защита от спама и сквернословия")
    btn4 = types.KeyboardButton("✅ Завершить создание бота")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, "Функции:", reply_markup=markup)




@bot.message_handler(content_types=['text'])
def act_li(message):
    if message.text == "❌ Удаление пользователя из канала":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton("Да")
        btn2 = types.KeyboardButton("Нет")
        markup.add(btn1, btn2)
        msg = bot.send_message(message.chat.id, "Вы хотите иметь функцию удаления пользователя из канала?",reply_markup=markup)
        bot.register_next_step_handler(msg, process_delete_user_step)

    elif message.text == "🔇 Заглушение пользователя на время":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton("Да")
        btn2 = types.KeyboardButton("Нет")
        markup.add(btn1, btn2)
        msg = bot.send_message(message.chat.id, "Вы хотите иметь функцию заглушения пользователя на время?",reply_markup=markup)
        bot.register_next_step_handler(msg, process_mute_user_step)

    elif message.text == "🤬 Защита от спама и сквернословия":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton("Да")
        btn2 = types.KeyboardButton("Нет")
        markup.add(btn1, btn2)
        msg = bot.send_message(message.chat.id, "Вы хотите иметь функцию фильтрации слов?",reply_markup=markup)
        bot.register_next_step_handler(msg, process_def_user_step)

    elif message.text == "✅ Завершить создание бота":
        bot.send_message(message.chat.id, text="Ваш бот создан")

    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммирован..")




def process_delete_user_step(message):
    if (message.text == "Да"):
        msg = bot.send_message(message.chat.id, "Какой командой будет проводиться удаление пользователя? (по умолчанию 'kick')")
        bot.register_next_step_handler(msg, save_delete_user_command)
    else:
        bot.send_message(message.chat.id, "Выберите другую функцию.")
        vibor(message)

def save_delete_user_command(message):
    delete_user_command = message.text
    bot.send_message(message.chat.id, f'Команда для удаления пользователя: {delete_user_command}. Учтите, что администраторов нельзя выгонять!')
    vibor(message)





def process_mute_user_step(message):
    if (message.text == "Да"):
        msg = bot.send_message(message.chat.id, "Какой командой будет проводиться заглушение пользователя? Учтите, что отмена заглушения будет проводится командой с добавлением un (по умолчанию 'mute' и 'unmute')")
        bot.register_next_step_handler(msg, save_mute_user_command)
    else:
        bot.send_message(message.chat.id, "Выберите другую функцию.")
        vibor(message)

def process2_time(message):
    mute_time = message.text
    bot.send_message(message.chat.id, f'Время: {mute_time}')
    vibor(message)

def save_mute_user_command(message):
    mute_user_command = message.text
    bot.send_message(message.chat.id, f'Команда для удаления пользователя: {mute_user_command}')
    msg = bot.send_message(message.chat.id, "Сколько времени будет длиться заглушение?")
    bot.register_next_step_handler(msg, process2_time)






def process_def_user_step(message):
    if (message.text == "Да"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton("Хватит")
        markup.add(btn1)
        msg = bot.send_message(message.chat.id, "Напишите, за какие слова пользователь будет блокироваться. Когда закончите, нажмите кнопку 'Хватит'",reply_markup=markup)
        bot.register_next_step_handler(msg, spisok_slov)
    else:
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








bot.infinity_polling(none_stop=True)