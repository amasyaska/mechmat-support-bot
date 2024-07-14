import random
import os
import logging
import telebot
from dotenv import load_dotenv, dotenv_values

from Database import Database

logging.basicConfig(filename="MechmatSupportAdministratorBot.log", level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')

load_dotenv()

ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")
bot = telebot.TeleBot(ADMIN_API_KEY)
db = Database()


def get_authorized_markup():
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.add(telebot.types.KeyboardButton("Відправити повідомлення для розсилки"))
    return markup

def get_unauthorized_markup():
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.add(telebot.types.KeyboardButton("Авторизуватись"))
    return markup

def get_back_markup():
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.add(telebot.types.KeyboardButton("Назад"))
    return markup

@bot.message_handler(commands=['start'])
def start_message(message):
    if (db.is_authorized_chat_id(message.chat.id)):
        bot.reply_to(message,
                     f"Привіт! Це бот для адміністрування бота-помічника @mechmatsupport_test_bot. Ви авторизовані для адміністрування.",
                    reply_markup=get_authorized_markup())
    else:
        bot.reply_to(message,
                     f"Привіт! Це бот для адміністрування бота-помічника @mechmatsupport_test_bot. Вам треба авторизуватися для адміністрування.",
                    reply_markup=get_unauthorized_markup())

def send_delivery_for_all_users(message):
    delivery_chat_id_list = db.get_delivery_chat_id_list()
    for chat_id in delivery_chat_id_list:
        bot_sender.send_message(chat_id, message)
    
@bot.message_handler(func=lambda message: True)
def universal_message(message):
    #try:
    if (db.is_authorized_chat_id(message.chat.id)):
        if (db.is_admin_delivering_by_chat_id(message.chat.id)):
            send_delivery_for_all_users(message.text)
            db.unset_admin_to_delivering_by_chat_id(message.chat.id)
        elif (message.text == "Відправити повідомлення для розсилки"):
            db.set_admin_to_delivering_by_chat_id(message.chat.id)
            bot.send_message(message.chat.id, "Введіть повідомлення для відправки")
        else:
            bot.send_message(message.chat.id, "Я не зрозумів Вашу команду.")
    elif (message.text == "сєкрєтний пароль 1337"):
        db.add_admin_by_chat_id(message.chat.id)
        bot.send_message(message.chat.id, "Пентагон взломан, ви авторизовані", reply_markup=get_authorized_markup())
    else:
        bot.send_message(message.chat.id, "Вам треба авторизуватися для адміністрування", reply_markup=get_unauthorized_markup())
    #except Exception as ex:
     #   logging.critical(f"{ex} happened...")

def main():
    bot.infinity_polling()
