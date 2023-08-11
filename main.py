import aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo
import webbrowser
import requests
import json

bot = Bot('6420992088:AAF54eNxwBs4727TSu8sl2QDGihUwQ9UZY4')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    #markup = types.InlineKeyboardMarkup(row_width=3)
    # = types.KeyboardButton('📖Меню', web_app=WebAppInfo(url='https://vadimirozz.github.io/kinda.html'))
    #btn2 = types.InlineKeyboardButton('👍🏻Отзывы', url='https://reviews.yandex.ru/ugcpub/cabinet')
    #btn4 = types.InlineKeyboardButton('🗑Корзина', callback_data='bin')
    #markup.add(btn1, btn2, btn4)
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton("WebApp", web_app=WebAppInfo(url='https://vadimirozz.github.io/kinda.html')))
    photo = open('p.jpg', 'rb')
    await bot.send_photo(message.chat.id, photo, caption="🤗 С теплом приветствуем вас! Откройте двери в мир "
                                                         "изысканных вкусов и непередаваемых эмоций. Приятного время "
                                                         "провождения!", reply_markup=markup)

@dp.message_handler(content_types=['web_app_data'])
async def web_app_get_info(message: types.Message):
    res = json.loads(message.web_app_data.data)
    await message.answer(f'Новый заказ! Имя: {res["name"]}. Email: {res["email"]}. Телефон: {res["phone"]}. Комментарий к заказу: {res["comment"]}')


executor.start_polling(dp)
