import telebot
import time
bot = telebot.TeleBot('6748343854:AAG0G4lj8aNIwvk66A9YR-f1F6x_0pxwtcY')

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для управления чатом. Напиши /help, чтобы узнать, что я умею.")

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "/kick - кикнуть пользователя\n/mute - замутить пользователя на определенное время\n/unmute - размутить пользователя\n/stats - показать статистику чата\n/selfstat - показать свою статистику")

#команда kick(опционально какой-либо другой, по задумке меняется в зависимости от желания пользователя)
@bot.message_handler(commands=['kick'])
def kick_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status
        if (user_status == 'administrator') or (user_status == 'creator'):
            bot.reply_to(message, "Невозможно кикнуть администратора.")
        else:
            bot.kick_chat_member(chat_id, user_id)
            bot.reply_to(message, f"Пользователь {message.reply_to_message.from_user.username} был удален.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите кикнуть.")

# Команда mute, аналогично опциональная
@bot.message_handler(commands=['mute'])
def mute_user(message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        user_status = bot.get_chat_member(chat_id, user_id).status
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно замутить администратора.")
        else:
            duration = 60 # Опциональное значение
            var = message.text.split()[1:]
            if args:
                try:
                    duration = int(var[0])
                except ValueError:
                    bot.reply_to(message, "Неправильный формат времени.")
                    return
                if duration < 1:
                    bot.reply_to(message, "Время должно быть положительным числом.")
                    return
                if duration > 1440:
                    bot.reply_to(message, "Максимальное время - 1 день.")
                    return
            bot.restrict_chat_member(chat_id, user_id, until_date=time.time()+duration*60)
            bot.reply_to(message, f"Пользователь {message.reply_to_message.from_user.username} заглушен на {duration} минут.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите замутить.")

# Аналогично для отмены заглушения
@bot.message_handler(commands=['unmute'])
def unmute_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        bot.restrict_chat_member(chat_id, user_id, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True)
        bot.reply_to(message, f"Пользователь {message.reply_to_message.from_user.username} размучен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите размутить.")


#список слов, который выбирается пользователем
words = ['анкета', 'ссылка', 'уникальное предложение']

# проверка на определенные слова 
def check_message(message):
    for word in words:
        if word in message.text.lower():
            return True
    return False

# обработчик сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # проверяем сообщение на наличие запрещенных слов
    if check_message(message):
        # если есть хотя бы одно запрещенное слово, кикаем пользователя
        bot.kick_chat_member(message.chat.id, message.from_user.id)
        bot.send_message(message.chat.id, f"Пользователь {message.from_user.username} был удален из чата за использование запрещенных слов")
    else:
        # если запрещенных слов нет, обрабатываем сообщение дальше
        print(message.text)



bot.infinity_polling(none_stop=True)
