import random
import os
import telebot
from dotenv import load_dotenv, dotenv_values

load_dotenv()

random_emojis_list = "😇🤩😍😜🤯"
API_KEY = os.getenv("API_KEY")
bot = telebot.TeleBot(API_KEY)

options_list = ["Абітурієнту", "Студенту", "ОП ММФ", "Корисні посилання", "Інше", "Дати приймальної комісії", "Перелік документів для вступу", "Перелік документів для поселення", "Гайд по спеціальностям", "Тритон", "Кафедри", "Пошти викладачів", "Департаменти", "Президія", "Як доєднатися?", "Маю ідею!", "ТГК ОП ММФ", "ТГК ММФ", "Інста ММФ", "Фейсбук ММФ", "Сайт студміста", "Сайт ММФ", "Карта факультету", "Карта до столовки на фрексі 😎"]

def get_start_markup():
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.add(telebot.types.KeyboardButton("Абітурієнту"))
    markup.add(telebot.types.KeyboardButton("Студенту"))
    markup.add(telebot.types.KeyboardButton("ОП ММФ"))
    markup.add(telebot.types.KeyboardButton("Корисні посилання"))
    markup.add(telebot.types.KeyboardButton("Інше"))
    markup.add(telebot.types.KeyboardButton("Показати мєм"))
    return markup

def get_abit_markup():
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.add(telebot.types.KeyboardButton("Дати приймальної комісії"))
    markup.add(telebot.types.KeyboardButton("Перелік документів для вступу"))
    markup.add(telebot.types.KeyboardButton("Перелік документів для поселення"))
    markup.add(telebot.types.KeyboardButton("Гайд по спеціальностям"))
    markup.add(telebot.types.KeyboardButton("Назад"))
    return markup

def get_student_markup():
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.add(telebot.types.KeyboardButton("Тритон"))
    markup.add(telebot.types.KeyboardButton("Кафедри"))
    markup.add(telebot.types.KeyboardButton("Пошти викладачів"))
    markup.add(telebot.types.KeyboardButton("Назад"))
    return markup

def get_op_markup():
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.add(telebot.types.KeyboardButton("Департаменти"))
    markup.add(telebot.types.KeyboardButton("Президія"))
    markup.add(telebot.types.KeyboardButton("Як доєднатися?"))
    markup.add(telebot.types.KeyboardButton("Маю ідею!"))
    markup.add(telebot.types.KeyboardButton("Назад"))
    return markup

def get_links_markup():
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.add(telebot.types.KeyboardButton("Сайт ММФ"))
    markup.add(telebot.types.KeyboardButton("Сайт студміста"))
    markup.add(telebot.types.KeyboardButton("Фейсбук ММФ"))
    markup.add(telebot.types.KeyboardButton("Інста ММФ"))
    markup.add(telebot.types.KeyboardButton("ТГК ММФ"))
    markup.add(telebot.types.KeyboardButton("ТГК ОП ММФ"))
    markup.add(telebot.types.KeyboardButton("Назад"))
    return markup

def get_other_markup():
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.add(telebot.types.KeyboardButton("Карта факультету"))
    markup.add(telebot.types.KeyboardButton("Карта до столовки на фрексі 😎"))
    markup.add(telebot.types.KeyboardButton("Назад"))
    return markup

def get_back_markup():
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.add(telebot.types.KeyboardButton("Назад"))
    return markup

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message,
                 f"Привіт! Це бот-помічник з механіко-математичного факультету КНУ {random_emojis_list[random.randint(0, len(random_emojis_list) - 1)]}. Тут ти можеш поставити питання або запропонувати ідею для покращення роботи факультету.",
                 reply_markup=get_start_markup())
    
@bot.message_handler(func=lambda message: True)
def universal_message(message):
    try:
        print(message.text)
    except Exception as ex:
        print(f"{ex} happened...")
    if (message.text == "Абітурієнту"):
        bot.send_message(message.chat.id, "Що саме Вас цікавить?", reply_markup=get_abit_markup())
    elif (message.text == "Студенту"):
        bot.send_message(message.chat.id, "Що саме Вас цікавить?", reply_markup=get_student_markup())
    elif (message.text == "ОП ММФ"):
        bot.send_message(message.chat.id, "Що саме Вас цікавить?", reply_markup=get_op_markup())
    elif (message.text == "Корисні посилання"):
        bot.send_message(message.chat.id, "Що саме Вас цікавить?", reply_markup=get_links_markup())
    elif (message.text == "Інше"):
        bot.send_message(message.chat.id, "Що саме Вас цікавить?", reply_markup=get_other_markup())
    elif (message.text == "Показати мєм"):
        bot.send_photo(message.chat.id, photo=open('mem.jpg', 'rb'), reply_markup=get_start_markup())
    elif (message.text in options_list):
        bot.send_message(message.chat.id, "*Цей розділ в розробці*", reply_markup=get_back_markup())
    elif (message.text == "Назад"):
        bot.send_message(message.chat.id,
                f"Привіт! Це бот-помічник з механіко-математичного факультету КНУ {random_emojis_list[random.randint(0, len(random_emojis_list) - 1)]}. Тут ти можеш поставити питання або запропонувати ідею для покращення роботи факультету.",
                 reply_markup=get_start_markup())
    else:
        bot.send_message(message.chat.id, "Я не зрозумів Вас. Введіть /start для початку роботи.")

if __name__ == "__main__":
    bot.infinity_polling()
