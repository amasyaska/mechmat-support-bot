import random
import os
import logging
import telebot
from dotenv import load_dotenv, dotenv_values

from Database import Database
import info

logging.basicConfig(filename="MechmatSupportBot.log", level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')

load_dotenv()

random_emojis_list = "😇🤩😍😜🤯😎"
API_KEY = os.getenv("API_KEY")
bot = telebot.TeleBot(API_KEY)
db = Database()

options_list = ["Абітурієнту", "Студенту", "ОП ММФ", "Корисні посилання", "Інше", "Дати приймальної комісії", "Перелік документів для вступу", "Перелік документів для поселення", "Гайд по спеціальностям", "Тритон", "Кафедри", "Пошти викладачів", "Департаменти", "Президія", "Як доєднатися?", "Маю ідею!", "ТГК ОП ММФ", "ТГК ММФ", "Інста ММФ", "Фейсбук ММФ", "Сайт студміста", "Сайт ММФ", "Карта факультету", "Карта до столовки на фрексі 😎"]


'''
def get_start_markup():
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.add(telebot.types.KeyboardButton("Абітурієнту"))
    markup.add(telebot.types.KeyboardButton("Студенту"))
    markup.add(telebot.types.KeyboardButton("ОП ММФ"))
    markup.add(telebot.types.KeyboardButton("Корисні посилання"))
    markup.add(telebot.types.KeyboardButton("Інше"))
    markup.add(telebot.types.KeyboardButton("Показати мєм"))
    markup.add(telebot.types.KeyboardButton("Підписатися на розсилку"))
    return markup
'''
'''
def get_abit_markup():
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.add(telebot.types.KeyboardButton("Дати приймальної комісії"))
    markup.add(telebot.types.KeyboardButton("Перелік документів для вступу"))
    markup.add(telebot.types.KeyboardButton("Перелік документів для поселення"))
    markup.add(telebot.types.KeyboardButton("Гайд по спеціальностям"))
    markup.add(telebot.types.KeyboardButton("Назад"))
    return markup
'''
'''
def get_student_markup():
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.add(telebot.types.KeyboardButton("Тритон"))
    markup.add(telebot.types.KeyboardButton("Кафедри"))
    markup.add(telebot.types.KeyboardButton("Пошти викладачів"))
    markup.add(telebot.types.KeyboardButton("Назад"))
    return markup
'''
    
'''
def get_op_markup():
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.add(telebot.types.KeyboardButton("Департаменти"))
    markup.add(telebot.types.KeyboardButton("Президія"))
    markup.add(telebot.types.KeyboardButton("Як доєднатися?"))
    markup.add(telebot.types.KeyboardButton("Маю ідею!"))
    markup.add(telebot.types.KeyboardButton("Назад"))
    return markup
'''
'''
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
'''
'''
def get_other_markup():
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.add(telebot.types.KeyboardButton("Карта факультету"))
    markup.add(telebot.types.KeyboardButton("Карта до столовки на фрексі 😎"))
    markup.add(telebot.types.KeyboardButton("Назад"))
    return markup
'''
'''
def get_back_markup():
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.add(telebot.types.KeyboardButton("Назад"))
    return markup
'''

def get_start_markup():
    keyboard = [
        [
            telebot.types.InlineKeyboardButton("Абітурієнту", callback_data="Абітурієнту"),
            telebot.types.InlineKeyboardButton("Студенту", callback_data="Студенту")],
        [
            telebot.types.InlineKeyboardButton("ОП ММФ", callback_data="ОП ММФ"),
            telebot.types.InlineKeyboardButton("Інше", callback_data="Інше")
        ],
        [telebot.types.InlineKeyboardButton("Корисні посилання", callback_data="Корисні посилання")],
        [telebot.types.InlineKeyboardButton("Підписатися на розсилку", callback_data="Підписатися на розсилку")],
        [telebot.types.InlineKeyboardButton("Показати мєм", callback_data="Показати мєм")]
    ]
    markup = telebot.types.InlineKeyboardMarkup(keyboard)
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    # Головне меню
    if (call.data == "Абітурієнту"):
        bot.send_message(call.message.chat.id, "Що саме Вас цікавить?", reply_markup=get_abit_markup())
    elif (call.data == "Студенту"):
        bot.send_message(call.message.chat.id, "Що саме Вас цікавить?", reply_markup=get_student_markup())
    elif (call.data == "ОП ММФ"):
        bot.send_message(call.message.chat.id, "Що саме Вас цікавить?", reply_markup=get_op_markup())
    elif (call.data == "Корисні посилання"):
        bot.send_message(call.message.chat.id, "Що саме Вас цікавить?", reply_markup=get_links_markup())
    elif (call.data == "Інше"):
        bot.send_message(call.message.chat.id, "Що саме Вас цікавить?", reply_markup=get_other_markup())
    elif (call.data == "Показати мєм"):
        bot.send_message(call.message.chat.id, "<a href='https://t.me/matematiki_enota'>математика для єнота</a>", parse_mode="HTML")
        bot.send_message(call.message.chat.id, "<a href='https://t.me/sixy_prime'>М[ζММ[ξ|ζ]]</a>", parse_mode="HTML", reply_markup=get_back_markup())
    elif (call.data == "Підписатися на розсилку"):
        bot.send_message(call.message.chat.id, "АГА ЩАС")

    # Абітурієнту
    elif (call.data == "Дати приймальної комісії"):
        bot.send_message(call.message.chat.id, info.dates_of_the_admissions_committee, reply_markup=get_back_markup())
    elif (call.data == "Перелік документів для вступу"):
        bot.send_message(call.message.chat.id, "Перелік документів для вступу:")
        bot.send_photo(call.message.chat.id, photo=open('resources/vstup_docs.png', 'rb'), reply_markup=get_back_markup())
    elif (call.data == "Перелік документів для поселення"):
        bot.send_message(call.message.chat.id, "Перелік документів для поселення:")
        bot.send_photo(call.message.chat.id, photo=open('resources/poselennya_docs.png', 'rb'), reply_markup=get_back_markup())

    # Корисні посилання
    elif (call.data == "Сайт ММФ"):
        bot.send_message(call.message.chat.id, "<a href='https://mechmat.knu.ua/'>Сайт ММФ</a>", parse_mode="HTML", reply_markup=get_back_markup())
    elif (call.data == "Фейсбук ММФ"):
        bot.send_message(call.message.chat.id, "<a href='https://www.facebook.com/mechmatKNU'>Фейсбук ММФ</a>", parse_mode="HTML", reply_markup=get_back_markup())
    elif (call.data == "Інста ММФ"):
        bot.send_message(call.message.chat.id, "<a href='https://www.instagram.com/mechmatknu?igsh=MTd4bTFjdHFkazZubw=='>Інста ММФ</a>", parse_mode="HTML", reply_markup=get_back_markup())
    elif (call.data == "Сайт студміста"):
        bot.send_message(call.message.chat.id, "<a href='https://studmisto.knu.ua/'>Сайт студміста</a>", parse_mode="HTML", reply_markup=get_back_markup())
    elif (call.data == "ТГК ОП ММФ"):
        bot.send_message(call.message.chat.id, "<a href='https://t.me/spmmf'>ТГК ОП ММФ</a>", parse_mode="HTML", reply_markup=get_back_markup())
    elif (call.data == "ТГК ММФ"):
        bot.send_message(call.message.chat.id, "<a href='https://t.me/mm_knu'>ТГК ММФ</a>", parse_mode="HTML", reply_markup=get_back_markup())
    elif (call.data == "Ютуб ММФ"):
        bot.send_message(call.message.chat.id, "<a href='https://www.youtube.com/channel/UCX4ENjo3GePeY5BV7htQVog'>Ютуб ММФ</a>", parse_mode="HTML", reply_markup=get_back_markup())

    # ОП ММФ
    elif (call.data == "Департаменти"):
        bot.send_message(call.message.chat.id, "Що саме Вас цікавить?", reply_markup=get_department_markup())
    elif (call.data == "Президія"):
        bot.send_message(call.message.chat.id, info.presidium, reply_markup=get_back_markup())

    # ОП ММФ -> Департаменти
    elif (call.data == "Культурно-мистецький"):
        bot.send_message(call.message.chat.id, info.cultural_department, reply_markup=get_back_markup())
    elif (call.data == "Інформаційний"):
        bot.send_message(call.message.chat.id, info.informational_department, reply_markup=get_back_markup())
    elif (call.data == "Спортивний"):
        bot.send_message(call.message.chat.id, info.department_of_sports, reply_markup=get_back_markup())
    elif (call.data == "Партнерства"):
        bot.send_message(call.message.chat.id, info.partnerships_department, reply_markup=get_back_markup())
    elif (call.data == "Робота з абітурієнтами"):
        bot.send_message(call.message.chat.id, info.abit_department, reply_markup=get_back_markup())

    # Інше
    elif (call.data == "Карта факультету"):
        bot.send_message(call.message.chat.id, "Карта факультету:")
        bot.send_photo(call.message.chat.id, photo=open('resources/faculty_map_1.jpg', 'rb'))
        bot.send_photo(call.message.chat.id, photo=open('resources/faculty_map_2.jpg', 'rb'), reply_markup=get_back_markup())
    elif (call.data == "Години роботи бібліотеки"):
        bot.send_message(call.message.chat.id, info.library_info, reply_markup=get_back_markup())

    elif (call.data == "На головну"):
        bot.send_message(call.message.chat.id,
                 f"Привіт! Це бот-помічник з механіко-математичного факультету КНУ {random_emojis_list[random.randint(0, len(random_emojis_list) - 1)]}. Тут ти можеш поставити питання або запропонувати ідею для покращення роботи факультету.",
                 reply_markup=get_start_markup())
    else:
        bot.send_message(call.message.chat.id,
                 f"Цей розділ в розробці 🙁.",
                 reply_markup=get_back_markup())

def get_abit_markup():
    keyboard = [
        [telebot.types.InlineKeyboardButton("Дати приймальної комісії", callback_data="Дати приймальної комісії")],
        [telebot.types.InlineKeyboardButton("Перелік документів для вступу", callback_data="Перелік документів для вступу")],
        [telebot.types.InlineKeyboardButton("Перелік документів для поселення", callback_data="Перелік документів для поселення")],
        [telebot.types.InlineKeyboardButton("Гайд по спеціальностям", callback_data="Гайд по спеціальностям")],
        [telebot.types.InlineKeyboardButton("На головну", callback_data="На головну")]
    ]
    markup = telebot.types.InlineKeyboardMarkup(keyboard)
    return markup

def get_student_markup():
    keyboard = [
        [telebot.types.InlineKeyboardButton("Тритон", callback_data="Тритон"),
         telebot.types.InlineKeyboardButton("Кафедри", callback_data="Кафедри")],
        [telebot.types.InlineKeyboardButton("Пошти викладачів", callback_data="Пошти викладачів")],
        [telebot.types.InlineKeyboardButton("На головну", callback_data="На головну")]
    ]
    markup = telebot.types.InlineKeyboardMarkup(keyboard)
    return markup

def get_op_markup():
    keyboard = [
        [telebot.types.InlineKeyboardButton("Департаменти", callback_data="Департаменти"),
         telebot.types.InlineKeyboardButton("Президія", callback_data="Президія")],
        [telebot.types.InlineKeyboardButton("Як доєднатися?", callback_data="Як доєднатися?")],
        [telebot.types.InlineKeyboardButton("Маю ідею!", callback_data="Маю ідею!?")],
        [telebot.types.InlineKeyboardButton("На головну", callback_data="На головну")]
    ]
    markup = telebot.types.InlineKeyboardMarkup(keyboard)
    return markup

def get_department_markup():
    keyboard = [
        [telebot.types.InlineKeyboardButton("Культурно-мистецький", callback_data="Культурно-мистецький")],
        [telebot.types.InlineKeyboardButton("Інформаційний", callback_data="Інформаційний")],
        [telebot.types.InlineKeyboardButton("Спортивний", callback_data="Спортивний")],
        [telebot.types.InlineKeyboardButton("Партнерства", callback_data="Партнерства")],
        [telebot.types.InlineKeyboardButton("Робота з абітурієнтами", callback_data="Робота з абітурієнтами")],
        [telebot.types.InlineKeyboardButton("На головну", callback_data="На головну")]
    ]
    markup = telebot.types.InlineKeyboardMarkup(keyboard)
    return markup


def get_links_markup():
    keyboard = [
        [telebot.types.InlineKeyboardButton("Сайт ММФ", callback_data="Сайт ММФ"),
         telebot.types.InlineKeyboardButton("Сайт студміста", callback_data="Сайт студміста")],
        [telebot.types.InlineKeyboardButton("Фейсбук ММФ", url="https://www.facebook.com/mechmatKNU"),
         telebot.types.InlineKeyboardButton("Інста ММФ", url="https://www.instagram.com/mechmatknu?igsh=MTd4bTFjdHFkazZubw==")],
        [telebot.types.InlineKeyboardButton("ТГК ММФ", callback_data="ТГК ММФ"),
         telebot.types.InlineKeyboardButton("ТГК ОП ММФ", callback_data="ТГК ОП ММФ")],
        [telebot.types.InlineKeyboardButton("Телеграм чат", callback_data="Телеграм чат"),
         telebot.types.InlineKeyboardButton("Ютуб ММФ", callback_data="Ютуб ММФ")],
        [telebot.types.InlineKeyboardButton("На головну", callback_data="На головну")]
    ]
    markup = telebot.types.InlineKeyboardMarkup(keyboard)
    return markup

def get_other_markup():
    keyboard = [
        [telebot.types.InlineKeyboardButton("Карта факультету", callback_data="Карта факультету")],
        [telebot.types.InlineKeyboardButton("Карта до столовки на фрексі 😎", callback_data="Карта до столовки на фрексі 😎")],
        [telebot.types.InlineKeyboardButton("Години роботи бібліотеки", callback_data="Години роботи бібліотеки")],
        [telebot.types.InlineKeyboardButton("На головну", callback_data="На головну")]
    ]
    markup = telebot.types.InlineKeyboardMarkup(keyboard)
    return markup

def get_back_markup():
    keyboard = [
        [telebot.types.InlineKeyboardButton("На головну", callback_data="На головну")]
    ]
    markup = telebot.types.InlineKeyboardMarkup(keyboard)
    return markup

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message,
                 f"Привіт! Це бот-помічник з механіко-математичного факультету КНУ {random_emojis_list[random.randint(0, len(random_emojis_list) - 1)]}. Тут ти можеш поставити питання або запропонувати ідею для покращення роботи факультету.",
                 reply_markup=get_start_markup())

def send_delivery_for_all_users(message):
    delivery_chat_id_list = db.get_delivery_chat_id_list()
    for chat_id in delivery_chat_id_list:
        bot.send_message(chat_id, message)

def send_delivery_for_all_users_interface():
    while True:
        send_delivery_for_all_users(input("Enter message: "))
    
@bot.message_handler(func=lambda message: True)
def universal_message(message):
    try:
        '''
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
        elif (message.text == "Підписатися на розсилку"):
            db.subscribe_user_delivery_by_chat_id(message.chat.id)
            bot.send_message(message.chat.id, "Готово! Тепер ви підписані на розсилку.", reply_markup=get_start_markup())
        elif (message.text in options_list):
            bot.send_message(message.chat.id, "*Цей розділ в розробці*", reply_markup=get_back_markup())
        elif (message.text == "Назад"):
            bot.send_message(message.chat.id,
                    f"Привіт! Це бот-помічник з механіко-математичного факультету КНУ {random_emojis_list[random.randint(0, len(random_emojis_list) - 1)]}. Тут ти можеш поставити питання або запропонувати ідею для покращення роботи факультету.",
                    reply_markup=get_start_markup())
        else:
        '''
        bot.send_message(message.chat.id, "Я не зрозумів Вас. Введіть /start для початку роботи.")
    except Exception as ex:
        logging.critical(f"{ex} happened...")

def main():
    bot.infinity_polling()

if __name__ == "__main__":
    main()
