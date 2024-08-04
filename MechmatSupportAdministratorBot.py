import random
import os
import logging
import telebot
from dotenv import load_dotenv, dotenv_values

from Database import Database

import info

logging.basicConfig(filename="MechmatSupportAdministratorBot.log", level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')

load_dotenv()

ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")
bot = telebot.TeleBot(ADMIN_API_KEY)
db = Database()

# MARKUPS

def get_authorized_markup():
    keyboard = [
        [telebot.types.InlineKeyboardButton("Відправити розсилку", callback_data="Відправити розсилку")],
        [telebot.types.InlineKeyboardButton("Активний зворотній зв'язок", callback_data="Активний зворотній зв'язок")],
        [telebot.types.InlineKeyboardButton("Увесь зворотній зв'язок", callback_data="Увесь зворотній зв'язок")]
    ]
    markup = telebot.types.InlineKeyboardMarkup(keyboard)
    return markup

def get_back_markup():
    keyboard = [
        [telebot.types.InlineKeyboardButton(info.main_page_button_text, callback_data=info.main_page_button_text)]
    ]
    markup = telebot.types.InlineKeyboardMarkup(keyboard)
    return markup

# CALLBACK QUERY HANDLERS

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if (not db.is_admin_by_chat_id(call.message.chat.id)):
        return None
    elif (call.data == "Відправити розсилку"):
        db.set_admin_state_by_chat_id(call.message.chat.id, 1)
        bot.send_message(call.message.chat.id, info.admin_delivery_text)

    elif (call.data == "Активний зворотній зв'язок"):
        db.db_cursor.execute(f'''SELECT *
                            FROM feedbackmessage
                            WHERE state=0;''')
        # iterate by db_cursor
        fetch_result = db.db_cursor.fetchone()
        print(fetch_result)
        while (fetch_result is not None):
            bot.send_message(call.message.chat.id, f"""Повідомлення #{fetch_result[0]}

"{fetch_result[2]}"

Статус: {status_to_str(fetch_result[3])}

Адміністратор, що надав відповідь: {answered_by(fetch_result[4])}""")
            fetch_result = db.db_cursor.fetchone()
        
    elif (call.data == "Увесь зворотній зв'язок"):
        db.db_cursor.execute(f'''SELECT *
                            FROM feedbackmessage;''')
        # iterate by db_cursor
        fetch_result = db.db_cursor.fetchone()
        while (fetch_result is not None):
            bot.send_message(call.message.chat.id, f"""Повідомлення #{fetch_result[0]}

"{fetch_result[2]}"

Статус: {status_to_str(fetch_result[3])}

Адміністратор, що надав відповідь: {answered_by(fetch_result[4])}""")
            fetch_result = db.db_cursor.fetchone()
        
    # BACK

    elif (call.data == info.main_page_button_text):
        db.set_admin_state_by_chat_id(call.message.chat.id, 0)
        bot.send_message(call.message.chat.id,
                     f"Привіт! Це бот для адміністрування бота-помічника @mechmatsupport_test_bot. Ви авторизовані для адміністрування.",
                    reply_markup=get_authorized_markup())

# MESSAGE HANDLERS

@bot.message_handler(commands=['start'])
def start_message(message):
    if (db.is_admin_by_chat_id(message.chat.id)):
        bot.reply_to(message,
                     f"Привіт! Це бот для адміністрування бота-помічника @mechmatsupport_test_bot. Ви авторизовані для адміністрування.",
                    reply_markup=get_authorized_markup())
    else:
        bot.reply_to(message,
                     f"Привіт! Це бот для адміністрування бота-помічника @mechmatsupport_test_bot. Вам треба авторизуватися для адміністрування.")
        
@bot.message_handler(commands=['answer'])
def answer_to_feedback(message):
    if (db.is_admin_by_chat_id(message.chat.id)):
        # getting feedback number
        number = message.text.split()[1]
        # getting answer
        message_content = message.text
        first_quote_index = message_content.index("\"") + 1
        message_content = message_content[::-1]
        last_quote_index = len(message_content) - message_content.index("\"") - 1
        feedback_content = message.text[first_quote_index:last_quote_index]

        # fetching data from db
        db.db_cursor.execute(f"""SELECT *
                            FROM feedbackmessage
                            WHERE number={number};""")
        fetch_result = db.db_cursor.fetchone()
        if (fetch_result is not None):
            bot_sender.send_message(fetch_result[1], f"""Відповідь від технічної підтримки на повідомлення з номером #{number}:
                                    
"{feedback_content}" """, reply_markup=get_back_markup())
            bot.reply_to(message, f"Відповідь на повідомлення #{number}:\n{feedback_content}\n\nвідправлено.",
                        reply_markup=get_authorized_markup())
        else:
            bot.reply_to(message, f"Сталася помилка: такого номеру повідомлення не існує",
                        reply_markup=get_authorized_markup())
    else:
        bot.reply_to(message,
                     f"Вам треба авторизуватися для адміністрування")
        
@bot.message_handler(commands=['create_one_time_password'])
def create_one_time_password_message(message):
    if (db.is_superadmin_by_chat_id(message.chat.id)):
        one_time_password = message.text.split()[1]
        db.create_one_time_password(message.chat.id, one_time_password)
        bot.reply_to(message, f"Одноразовий пароль був успішно створений. Ви можете використати його для того, щоб додати адміністратора. Адміністратор має ввести команду \"/password {one_time_password}\"",
                    reply_markup=get_authorized_markup())
    else:
        bot.reply_to(message,
                     f"Вам треба авторизуватися для адміністрування")
        

@bot.message_handler(commands=['password'])
def password_message(message):
    one_time_password = message.text.split()[1]
    if (db.is_admin_by_chat_id(message.chat.id)):
        bot.reply_to(message, f"Ви вже авторизовані для адміністрування",
                    reply_markup=get_authorized_markup())
    elif (db.is_one_time_password(one_time_password)):
        db.add_admin_by_chat_id(message.chat.id)
        db.delete_one_time_password(one_time_password)
        bot.reply_to(message,
                     f"Готово! Тепер ви авторизовані для адміністрування",
                     reply_markup=get_authorized_markup())
    else:
        bot.reply_to(message,
                     f"Вам треба авторизуватися для адміністрування")
    
@bot.message_handler(func=lambda message: True)
def universal_message(message):
    #try:
    if (db.is_admin_by_chat_id(message.chat.id) and db.get_admin_state_by_chat_id(message.chat.id) == 0):
        bot.send_message(message.chat.id, f"Я не зрозумів команду. Це бот для адміністрування бота-помічника @mechmatsupport_test_bot. Ви авторизовані для адміністрування.",
                       reply_markup=get_authorized_markup())
    elif (db.is_admin_by_chat_id(message.chat.id) and db.get_admin_state_by_chat_id(message.chat.id) == 1):
        db.set_admin_state_by_chat_id(message.chat.id, 0)
        send_delivery_for_all_users(message.text)
        bot.send_message(message.chat.id, f"Розсилку відправлено!",
                         reply_markup=get_authorized_markup())
    else:
        bot.send_message(message.chat.id, "Я не зрозумів команду. Вам треба авторизуватися для адміністрування")
    #except Exception as ex:
     #   logging.critical(f"{ex} happened...")

# FUNCTIONS

def send_delivery_for_all_users(message):
    db.db_cursor.execute(f'''SELECT chat_id
                            FROM mechmatsupportbotuser
                            WHERE delivery=TRUE;''')
    for chat_id in db.db_cursor:
        bot_sender.send_message(chat_id[0], message)

def status_to_str(n: int) -> str:
    status_list = ["Активний", "Відповідь надано", "Закритий"]
    return status_list[n]

def answered_by(chat_id: int) -> str:
    return "Відповідь не надана" if chat_id == -1 else chat_id

def main():
    bot.infinity_polling()
