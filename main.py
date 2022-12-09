import logging
from pprint import pprint
import random

import config
import markups
import tutorial_text

from aiogram import Bot, Dispatcher, executor, types

from data import db_session
from data.channels import Channel
from data.users import User
from data.payments import Payment
from data.lessons import Lesson
from data.schools import School
from data.admin_channels import AdminChannel

from aiogram.types.message import ContentType

from pyqiwip2p import QiwiP2P

logging.basicConfig(level=logging.INFO)


bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)
strogage_for_channel = dict()
strogage_for_bill = dict()
strogage_status = dict()

p2p = QiwiP2P(auth_key=config.QIWI_TOKEN)


def is_number(_str):
    try:
        int(_str)
        return True
    except ValueError:
        return False


def check_sub_channel(chat_member):
    if chat_member['status'] != 'left':
        return True
    else:
        return False


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    if message.chat.type == 'private':
        if not check_sub_channel(await bot.get_chat_member(chat_id=config.CHANNEL_ID, user_id=message.from_user.id)):
            await bot.send_message(message.from_user.id, 'Сначала подпишись!', reply_markup=markups.check_sub_menu)
            return
    strogage_status[message.from_user.id] = None
    db_sess = db_session.create_session()
    if db_sess.query(User).filter(User.user_id == message.from_user.id).all():
        await bot.send_message(message.from_user.id,
                               'Снова здесь?', reply_markup=markups.start_menu)
    else:
        await register_user(message, db_sess)


@dp.callback_query_handler(text='sub_channel_done')
async def sub_channel_done(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    if check_sub_channel(await bot.get_chat_member(chat_id=config.CHANNEL_ID, user_id=message.from_user.id)):
        await register_user(message, db_session.create_session())
    else:
        await bot.send_message(message.from_user.id, 'Сначала подпишись!', reply_markup=markups.check_sub_menu)


async def register_user(message: types.Message, db_sess):
    user = User()
    user.user_id = message.from_user.id
    user.username = message.from_user.username
    db_sess.add(user)
    db_sess.commit()
    await tutorial_1(message)


async def tutorial_1(message: types.Message):
    with open('img/tutorial/tutorial_1.png', 'rb') as photo:
        await bot.send_photo(message.from_user.id,
                             caption=tutorial_text.tutorial_1,
                             photo=photo,
                             reply_markup=markups.tutorial_1)


@dp.callback_query_handler(text='tutorial_2')
async def tutorial_2(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    with open('img/tutorial/tutorial_2.png', 'rb') as photo:
        await bot.send_photo(message.from_user.id,
                             caption=tutorial_text.tutorial_2,
                             photo=photo,
                             reply_markup=markups.tutorial_2)


@dp.callback_query_handler(text='tutorial_3')
async def tutorial_3(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    with open('img/tutorial/tutorial_3.png', 'rb') as photo:
        await bot.send_photo(message.from_user.id,
                             caption=tutorial_text.tutorial_3,
                             photo=photo,
                             reply_markup=markups.tutorial_3)


@dp.callback_query_handler(text='tutorial_4')
async def tutorial_3(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, 'Лови менюшку', reply_markup=markups.start_menu)


@dp.callback_query_handler(text_contains='lesson')
async def lesson_callback(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    strogage_status[call.from_user.id] = None

    datas = call.data.split('_')
    choose_school_menu = markups.get_schools(datas[0])

    db_sess = db_session.create_session()
    lesson = db_sess.query(Lesson).filter(Lesson.lesson_title == datas[0]).first()
    if lesson:
        img_path = lesson.img_path if lesson.img_path else 'img/none.png'
        with open(img_path, 'rb') as photo:
            await bot.send_photo(call.message.chat.id,
                                 photo=photo,
                                 caption=f'{datas[0].capitalize()} >> Онлайн Школа\n\n'
                                         f'Выбери Онлайн-Школу, по которой хочешь обучаться',
                                 reply_markup=choose_school_menu)
    else:
        await bot.send_message(call.from_user.id,
                               f'{datas[0].capitalize()} >> Онлайн Школа\n\n'
                               f'Выбери Онлайн-Школу, по которой хочешь обучаться',
                               reply_markup=choose_school_menu)


@dp.callback_query_handler(text_contains='school')
async def school_callback(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    strogage_status[call.from_user.id] = 'school'

    datas = call.data.split('_')
    choose_months_menu = markups.get_months(datas[0],
                                            datas[1])
    db_sess = db_session.create_session()
    school = db_sess.query(School).filter(School.school_title == datas[1]).first()

    img_path = school.img_path if school.img_path else 'img/none.png'

    with open(img_path, 'rb') as photo:
        await bot.send_photo(call.from_user.id,
                            photo=photo,
                            caption=f"{datas[0].capitalize()} >> {datas[1].capitalize()} >> Месяц\n\n"
                                    f"Отлично, теперь выбери месяц, который хочешь получить",
                            reply_markup=choose_months_menu)


@dp.callback_query_handler(text_contains='month')
async def month_callback(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    strogage_status[call.from_user.id] = 'month'
    datas = call.data.split('_')

    db_sess = db_session.create_session()
    channel = db_sess.query(Channel).filter(Channel.school_title == datas[2],
                                            Channel.lesson_title == datas[1],
                                            Channel.month_title == datas[0]).first()
    strogage_for_channel[call.from_user.id] = channel

    img_path = channel.schedule_img_path if channel.schedule_img_path else 'img/none.png'

    with open(img_path, 'rb') as photo:
        await bot.send_photo(call.message.chat.id,
                             photo=photo,
                             caption="Ты уверен?",
                             reply_markup=markups.month_pay_menu)


@dp.callback_query_handler(text='go_to_pay')
async def pay_handler(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    comment = str(call.from_user.id) + '_' + str(random.randint(1000, 9999))
    bill = p2p.bill(amount=5, lifetime=15, comment=comment)
    strogage_for_bill[call.from_user.id] = bill

    await bot.send_message(call.from_user.id,
                           f'Вам нужно отправить 5 руб. на счет QIWI\n'
                           f'Ссылку: {bill.pay_url}, указав комментарий к оплате: {comment}',
                           reply_markup=markups.buy_menu(url=bill.pay_url, bill=bill.bill_id))
    # PRICE = types.LabeledPrice(label="1 месяц канала", amount=150 * 100)
    #
    # await bot.send_invoice(call.from_user.id,
    #                        title="Покупка Курса",
    #                        description=f'Курс по предмету "{channel.lesson_title.capitalize()}",'
    #                                    f' от школы "{channel.school_title.capitalize()}" за {channel.month_title}',
    #                        provider_token=config.PAYMASTER_TOKEN,
    #                        currency="rub",
    #                        photo_url='https://ie.wampi.ru/2022/10/27/sell_photo.png',
    #                        photo_width=416,
    #                        photo_height=234,
    #                        photo_size=416,
    #                        is_flexible=False,
    #                        prices=[PRICE],
    #                        start_parameter="one-month-subscription",
    #                        payload="test-invoice-payload")


@dp.callback_query_handler(text_contains='without_money')
async def without_money(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, 'щас')
    await successful_payment(callback)


@dp.callback_query_handler(text_contains='check_')
async def check(callback: types.CallbackQuery):
    bill = str(callback.data[6:])
    if str(p2p.check(bill_id=bill).status) == 'PAID':
        await successful_payment(callback)
    else:
        await bot.send_message(callback.from_user.id,
                               'Вы не оплатили счет!',
                               reply_markup=markups.buy_menu(False, bill=bill))


@dp.callback_query_handler(text='go_back')
async def go_back_callback(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.from_user.id, 'Пока-что не готов?')
    await bot.send_message(call.from_user.id, 'Посмотри как мы сливаем реальные курсы:')
    await bot.send_message(call.from_user.id, '*Здесь можно поставить ссылки на бесплатные сливы или же на канал с отзывами')


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


async def successful_payment(message: types.CallbackQuery):
    db_sess = db_session.create_session()
    payment = Payment()
    payment.user_id = message.from_user.id
    payment.channel_id = strogage_for_channel[message.from_user.id].channel_id
    payment.price = 150
    db_sess.add(payment)
    db_sess.commit()

    channel_invite_link = await bot.create_chat_invite_link(
        chat_id=str(strogage_for_channel[message.from_user.id].channel_id), member_limit=1)

    await bot.send_message(message.from_user.id,
                           f'Держи ссылку, но аккуратней, она одноразовая\n\n{channel_invite_link.invite_link}')
    await bot.send_message(message.from_user.id,
                           f"Платёж пользователя прошел успешно!")


@dp.message_handler()
async def bot_message(message: types.Message):
    if check_sub_channel(await bot.get_chat_member(chat_id=config.CHANNEL_ID, user_id=message.from_user.id)):
        strogage_status[message.from_user.id] = None
        if message.from_user.id == 5471950124 \
                and message.text.lower().startswith('добавить в бд'):
            data = message.text.split(';')

            db_sess = db_session.create_session()
            channel = Channel()
            channel.channel_id = data[1].lower()
            channel.school_title = data[2].lower()
            channel.month_title = data[3].lower()
            channel.lesson_title = data[4].lower()
            channel.schedule_img_path = data[5].lower()
            db_sess.add(channel)
            db_sess.commit()

            await bot.send_message(message.from_user.id, f'Добавил:'
                                                         f'channel_id: {channel.channel_id}\n'
                                                         f'school_title: {channel.school_title}\n'
                                                         f'month_title: {channel.month_title}\n'
                                                         f'lesson_title: {channel.lesson_title}'
                                                         f'img: {channel.schedule_img_path}')

            # добавить в бд;-1001810340070;100-балльный;октябрь;математика
        elif message.text == 'ЕГЭ':
            choose_lesson_menu = markups.get_lessons()
            await bot.send_message(
                message.from_user.id,
                'Перед тобой курсы ЕГЭ 2023 года.\n'
                'Выбери предмет', reply_markup=choose_lesson_menu)
        elif message.text == 'Гарантии':
            await bot.send_message(message.from_user.id,
                                   'Здесь будут гарантии')
        elif message.text == 'FAQ':
            await bot.send_message(message.from_user.id,
                                   'Здесь будет вопрос-ответ')
        else:
            await bot.send_message(message.from_user.id,
                                   'не понимаю')
    else:
        await bot.send_message(message.from_user.id, 'Где твоя подписка, вац?', reply_markup=markups.check_sub_menu)


@dp.channel_post_handler()
async def channel_post_message(message: types.Message):
    db_sess = db_session.create_session()
    if not db_sess.query(AdminChannel).filter(AdminChannel.channel_id == message.chat.id).all():
        admin_channel = AdminChannel()
        admin_channel.channel_id = message.chat.id
        admin_channel.channel_title = message.chat.title
        db_sess.add(admin_channel)
        db_sess.commit()


if __name__ == "__main__":
    db_session.global_init("db/ege_bot.db")
    executor.start_polling(dp, skip_updates=False)
