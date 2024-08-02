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


def get_start_markup():
    keyboard = [
        [
            telebot.types.InlineKeyboardButton("Абітурієнту ☀️", callback_data="Абітурієнту"),
            telebot.types.InlineKeyboardButton("Студенту 👨‍🎓", callback_data="Студенту")],
        [telebot.types.InlineKeyboardButton("Офіс Представників ММФ 🏛️", callback_data="ОП ММФ")],
        [telebot.types.InlineKeyboardButton("Інше 🦝", callback_data="Інше")],
        [telebot.types.InlineKeyboardButton("Корисні посилання", callback_data="Корисні посилання")],
        [telebot.types.InlineKeyboardButton("Підписатися на розсилку 📬", callback_data="Підписатися на розсилку")],
        [telebot.types.InlineKeyboardButton("Показати мєм 🐧", callback_data="Показати мєм")]
    ]
    markup = telebot.types.InlineKeyboardMarkup(keyboard)
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    # check if user exists:
    if (not db.is_user_exists_by_chat_id(call.message.chat.id)):
        db.add_user_by_chat_id(call.message.chat.id)
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
        bot.send_message(call.message.chat.id, info.tg_channel_matematika_dlya_ienota_html, parse_mode="HTML")
        bot.send_message(call.message.chat.id, info.tg_channel_sixy_prime_html, parse_mode="HTML", reply_markup=get_back_markup())
    elif (call.data == "Підписатися на розсилку"):
        db.set_user_delivery_by_chat_id(call.message.chat.id, True)
        bot.send_message(call.message.chat.id, "Ви підписані на розсилку, перевірити статус: /check_delivery")

    # Абітурієнту
    elif (call.data == "Дати приймальної комісії"):
        bot.send_message(call.message.chat.id, info.dates_of_the_admissions_committee, reply_markup=get_back_markup())
    elif (call.data == "Перелік документів для вступу"):
        bot.send_message(call.message.chat.id, info.documenty_dlya_vstupu, reply_markup=get_back_markup())
        # bot.send_photo(call.message.chat.id, photo=open('resources/vstup_docs.png', 'rb'), reply_markup=get_back_markup())
    elif (call.data == "Перелік документів для поселення"):
        bot.send_message(call.message.chat.id, info.documenty_dlya_poselennya, parse_mode="HTML", reply_markup=get_back_markup())
        # bot.send_photo(call.message.chat.id, photo=open('resources/poselennya_docs.png', 'rb'), reply_markup=get_back_markup())

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

    elif (call.data == info.main_page_button_text):
        bot.send_message(call.message.chat.id,
                 f"Привіт! Це бот-помічник з механіко-математичного факультету КНУ {random_emojis_list[random.randint(0, len(random_emojis_list) - 1)]}. Тут ти можеш поставити питання або запропонувати ідею для покращення роботи факультету.",
                 reply_markup=get_start_markup())
    else:
        bot.send_message(call.message.chat.id,
                 f"Цей розділ в розробці 🙁.",
                 reply_markup=get_back_markup())

def get_abit_markup():
    keyboard = [
        [telebot.types.InlineKeyboardButton("Дати приймальної комісії 📅", callback_data="Дати приймальної комісії")],
        [telebot.types.InlineKeyboardButton("Перелік документів для вступу 📄", callback_data="Перелік документів для вступу")],
        [telebot.types.InlineKeyboardButton("Перелік документів для поселення 📃", callback_data="Перелік документів для поселення")],
        [telebot.types.InlineKeyboardButton("Гайд по спеціальностям ⚙️", callback_data="Гайд по спеціальностям")],
        [telebot.types.InlineKeyboardButton(info.main_page_button_text, callback_data=info.main_page_button_text)]
    ]
    markup = telebot.types.InlineKeyboardMarkup(keyboard)
    return markup

def get_student_markup():
    keyboard = [
        [telebot.types.InlineKeyboardButton("Тритон", callback_data="Тритон"),
         telebot.types.InlineKeyboardButton("Кафедри", callback_data="Кафедри")],
        [telebot.types.InlineKeyboardButton("Пошти викладачів", callback_data="Пошти викладачів")],
        [telebot.types.InlineKeyboardButton(info.main_page_button_text, callback_data=info.main_page_button_text)]
    ]
    markup = telebot.types.InlineKeyboardMarkup(keyboard)
    return markup

def get_op_markup():
    keyboard = [
        [telebot.types.InlineKeyboardButton("Департаменти 🏬", callback_data="Департаменти"),
         telebot.types.InlineKeyboardButton("Президія 💼", callback_data="Президія")],
        [telebot.types.InlineKeyboardButton("Як доєднатися?", callback_data="Як доєднатися?")],
        [telebot.types.InlineKeyboardButton("Маю ідею! 💡", callback_data="Маю ідею!?")],
        [telebot.types.InlineKeyboardButton(info.main_page_button_text, callback_data=info.main_page_button_text)]
    ]
    markup = telebot.types.InlineKeyboardMarkup(keyboard)
    return markup

def get_department_markup():
    keyboard = [
        [telebot.types.InlineKeyboardButton("Культурно-мистецький 🥳", callback_data="Культурно-мистецький")],
        [telebot.types.InlineKeyboardButton("Інформаційний 🔊", callback_data="Інформаційний")],
        [telebot.types.InlineKeyboardButton("Спортивний ⚽", callback_data="Спортивний")],
        [telebot.types.InlineKeyboardButton("Партнерства 🤝", callback_data="Партнерства")],
        [telebot.types.InlineKeyboardButton("Робота з абітурієнтами ✌️", callback_data="Робота з абітурієнтами")],
        [telebot.types.InlineKeyboardButton(info.main_page_button_text, callback_data=info.main_page_button_text)]
    ]
    markup = telebot.types.InlineKeyboardMarkup(keyboard)
    return markup


def get_links_markup():
    keyboard = [
        [telebot.types.InlineKeyboardButton("Сайт ММФ", url=info.mmf_url),
         telebot.types.InlineKeyboardButton("Сайт студміста", url=info.studmisto_url)],
        [telebot.types.InlineKeyboardButton("Фейсбук ММФ", url=info.mmf_facebook_url),
         telebot.types.InlineKeyboardButton("Інста ММФ", url=info.mmf_instagram_url)],
        [telebot.types.InlineKeyboardButton("Телеграм канал ММФ", url=info.mmf_tg_channel),
         telebot.types.InlineKeyboardButton("Телеграм канал ОП ММФ", url=info.mmf_op_tg_channel)],
        [telebot.types.InlineKeyboardButton("Телеграм чат", url=info.mmf_tg_abit_chat),
         telebot.types.InlineKeyboardButton("Ютуб ММФ", url=info.mmf_youtube)],
        [telebot.types.InlineKeyboardButton(info.main_page_button_text, callback_data=info.main_page_button_text)]
    ]
    markup = telebot.types.InlineKeyboardMarkup(keyboard)
    return markup

def get_other_markup():
    keyboard = [
        [telebot.types.InlineKeyboardButton("Карта факультету 🗺️", callback_data="Карта факультету")],
        [telebot.types.InlineKeyboardButton("Карта до столовки на фрексі 😎", callback_data="Карта до столовки на фрексі 😎")],
        [telebot.types.InlineKeyboardButton("Години роботи бібліотеки 📚", callback_data="Години роботи бібліотеки")],
        [telebot.types.InlineKeyboardButton(info.main_page_button_text, callback_data=info.main_page_button_text)]
    ]
    markup = telebot.types.InlineKeyboardMarkup(keyboard)
    return markup

def get_back_markup():
    keyboard = [
        [telebot.types.InlineKeyboardButton(info.main_page_button_text, callback_data=info.main_page_button_text)]
    ]
    markup = telebot.types.InlineKeyboardMarkup(keyboard)
    return markup

@bot.message_handler(commands=['check_delivery'])
def start_message(message):
    if (not db.is_user_exists_by_chat_id(message.chat.id)):
        db.add_user_by_chat_id(message.chat.id)
    if (db.get_user_delivery_by_chat_id(message.chat.id) == 1):
        bot.reply_to(message, "Ви підписані на розсилку", reply_markup=get_back_markup())
    else:
        bot.reply_to(message, "Ви не підписані на розсилку", reply_markup=get_back_markup())

@bot.message_handler(commands=['start'])
def start_message(message):
    if (not db.is_user_exists_by_chat_id(message.chat.id)):
        db.add_user_by_chat_id(message.chat.id)
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
    if (not db.is_user_exists_by_chat_id(message.chat.id)):
        db.add_user_by_chat_id(message.chat.id)
    try:
        bot.send_message(message.chat.id, "Я не зрозумів Вас. Введіть /start для початку роботи.", reply_markup=get_back_markup())
    except Exception as ex:
        logging.critical(f"{ex} happened...")

def main():
    bot.infinity_polling()

if __name__ == "__main__":
    main()
