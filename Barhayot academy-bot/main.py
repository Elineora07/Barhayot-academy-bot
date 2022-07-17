import sqlite3
import telebot
from telebot.types import *
import random

token1 = "5183869458:AAHfbhtoI5SsUSdlMiSuUrIpuoe-zkiZUac"
usernmae1 = "@seihguies234_bot"
bot = telebot.TeleBot(token1)


def phone():
    phone_ = []
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    for row in cur.execute('SELECT * FROM user ORDER BY user_id'):
        phone_ += [row[2]]
    return phone_


def text():
    text_ = ""
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    for row in cur.execute('SELECT * FROM user ORDER BY user_id'):
        text_ += f"{row[1]}  {row[2]}\n"
    return text_


def user_table():
    user = []
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    for row in cur.execute('SELECT * FROM user ORDER BY user_id'):
        user += [row[0]]
    return user


def admin_table():
    admin = []
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    for row in cur.execute('SELECT * FROM admin ORDER BY user_id'):
        admin += [row[0]]
    return admin


def admin_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = KeyboardButton("Admin qo'shish")
    btn2 = KeyboardButton("Ro'yxatdan o'tkanlar")
    btn3 = KeyboardButton("Random")
    return keyboard.add(btn1, btn2, btn3)


def registration_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton("Ro'yxatdan o'tish")
    return keyboard.add(btn)


@bot.message_handler(commands="start")
def start(message):
    user_id = message.chat.id
    admin = admin_table()
    if user_id not in admin:
        if user_id not in user_table():
            con = sqlite3.connect("data.db")
            cur = con.cursor()
            cur.execute(f"INSERT INTO user VALUES ({user_id}, '------', '------')")
            con.commit()
        bot.send_message(user_id, "Assalomu alaykum. xush kelibsiz!!!.Siz Barhayot academy ni rasmiy botiga kirdingiz aksiyaga qo'shilish uchun ro'yxatdan o'ting", reply_markup=registration_keyboard())
    else:
        bot.send_message(user_id, "Assalomu aleykum", reply_markup=admin_keyboard())


def create_phone(message):
    user_id = message.chat.id
    phone = message.text
    if phone.startswith("+998") and len(phone) == 13 and phone[1:].isdigit():
        con = sqlite3.connect("data.db")
        cur = con.cursor()
        print(phone)
        cur.execute(f"UPDATE user SET phone = '{phone}' WHERE user_id = {user_id}")
        con.commit()
        bot.send_message(user_id, "Siz Ro'yxatga olindigiz")
    else:
        bot.send_message(user_id, "Boshqatdan kiriting")
        bot.register_next_step_handler(message, create_phone)


def create_name(message):
    name = message.text
    user_id = message.chat.id
    ism = name.split(" ")
    user = user_table()
    text = ""
    if name != "/start":
        for s in ism:
            text += f"{s} "
        if len(ism) in [2, 3, 4]:
            if ism[0].isalpha() and ism[1].isalpha():
                con = sqlite3.connect("data.db")
                cur = con.cursor()
                cur.execute(f"UPDATE user SET Full_name = '{text}' WHERE user_id = {message.chat.id}")
                con.commit()
                bot.send_message(user_id, "Telefon raqamni kiriting")
                bot.register_next_step_handler(message, create_phone)
            else:
                bot.send_message(user_id, "Iltimos boshqatdan kirting")
                bot.register_next_step_handler(message, create_name)

        else:
            bot.send_message(user_id, "Iltimos boshqatdan kirting")
            bot.register_next_step_handler(message, create_name)


@bot.message_handler(func=lambda x: x.text == "Ro'yxatdan o'tish")
def registration(message):
    user_id = message.chat.id
    bot.send_message(user_id, "Ism familiyani kiriting", reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(message, create_name)


def add(message):
    if message.forward_from:
        user_id = message.forward_from.id
        if user_id not in admin_table():
            con = sqlite3.connect("data.db")
            cur = con.cursor()
            cur.execute(f"INSERT INTO admin VALUES ({user_id})")
            con.commit()
        bot.send_message(message.chat.id, "Qo'shildi")
    else:
        bot.send_message(message.chat.id, "Boshqatdan urining")


@bot.message_handler(func=lambda x: x.text == "Admin qo'shish")
def admin_add(message):
    user_id = message.chat.id
    bot.send_message(user_id, "Qo'shmoqchi bo'lgan admindan birorta habar forward qiling")
    bot.register_next_step_handler(message, add)


@bot.message_handler(func=lambda x: x.text == "Ro'yxatdan o'tkanlar")
def table_register_table(message):
    bot.send_message(message.chat.id, text())


@bot.message_handler(func=lambda x: x.text == "Random")
def random_(message):
    phone_ = phone()
    user = random.choice(phone_)
    bot.send_message(message.chat.id, user)


bot.polling()
