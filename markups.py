from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from data import db_session
from data.channels import Channel


check_sub_menu = InlineKeyboardMarkup(row_width=1)

btn_url_channel = InlineKeyboardButton(text='Подписаться', url='https://t.me/egetgsliv')
btn_done_sub = InlineKeyboardButton(text='Проверить подписку', callback_data='sub_channel_done')

check_sub_menu.insert(btn_url_channel)
check_sub_menu.insert(btn_done_sub)

start_menu = ReplyKeyboardMarkup(resize_keyboard=True)
EGE_btn = KeyboardButton('ЕГЭ')
garanties_btn = KeyboardButton('Гарантии')
FAQ_btn = KeyboardButton('FAQ')

start_menu.insert(EGE_btn)
start_menu.insert(garanties_btn)
start_menu.insert(FAQ_btn)


month_pay_menu = InlineKeyboardMarkup(resize_keyboard=True)
go_to_pay_btn = InlineKeyboardButton(text='Да, перейти к оплате', callback_data='go_to_pay')
go_back = InlineKeyboardButton(text='Нет, я ещё не готов!', callback_data='go_back')

month_pay_menu.insert(go_to_pay_btn)
month_pay_menu.insert(go_back)


###

tutorial_1 = InlineKeyboardMarkup().insert(InlineKeyboardButton(text='Далее', callback_data='tutorial_2'))
tutorial_2 = InlineKeyboardMarkup().insert(InlineKeyboardButton(text='Далее', callback_data='tutorial_3'))
tutorial_3 = InlineKeyboardMarkup().insert(InlineKeyboardButton(text='Вперед к 80+ баллам', callback_data='tutorial_4'))

###


def get_lessons():
    choose_lesson_menu = InlineKeyboardMarkup(row_width=2)
    db_sess = db_session.create_session()
    data = db_sess.query(Channel).all()
    all_temps = set()
    for i in data:
        if i.lesson_title not in all_temps:
            temp = InlineKeyboardButton(text=i.lesson_title.capitalize(),
                                        callback_data=f'{i.lesson_title}_lesson')
            choose_lesson_menu.insert(temp)
            all_temps.add(i.lesson_title)
    return choose_lesson_menu


def get_schools(lesson_title):
    choose_school_menu = InlineKeyboardMarkup(row_width=2)
    db_sess = db_session.create_session()
    data = db_sess.query(Channel).filter(Channel.lesson_title == lesson_title).all()
    all_temps = set()
    for i in data:
        if i.school_title not in all_temps:
            temp = InlineKeyboardButton(text=i.school_title.capitalize(),
                                        callback_data=f'{i.lesson_title}_{i.school_title}_school')
            choose_school_menu.insert(temp)
            all_temps.add(i.school_title)
    return choose_school_menu


def get_months(lesson_title, school_title):
    choose_month_menu = InlineKeyboardMarkup()
    db_sess = db_session.create_session()
    data = db_sess.query(Channel).filter(Channel.lesson_title == lesson_title,
                                         Channel.school_title == school_title).all()
    for i in data:
        temp = InlineKeyboardButton(text=i.month_title.capitalize(),
                                    callback_data=f'{i.month_title}_{i.lesson_title}_{i.school_title}_month')
        choose_month_menu.insert(temp)
    return choose_month_menu

###


def buy_menu(isUrl=True, url='', bill=''):
    qiwiMenu = InlineKeyboardMarkup(row_width=1)

    if isUrl:
        btn_url_qiwi = InlineKeyboardButton(text='Ссылка на оплату', url=url)
        qiwiMenu.insert(btn_url_qiwi)

    btn_check_qiwi = InlineKeyboardButton(text='Проверить оплату', callback_data='check_' + bill)
    qiwiMenu.insert(btn_check_qiwi)
    qiwiMenu.insert(InlineKeyboardButton(text='Дай без оплаты!', callback_data='without_money'))
    return qiwiMenu