import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import CallbackQuery
from aiogram.types.web_app_info import WebAppInfo
import json
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage


async def first_bot(token, queue, dp):
    bot = Bot(token)

    @dp.message_handler(commands=['start'])
    async def start_message(message: types.Message, state: FSMContext):
        markup = types.ReplyKeyboardMarkup()
        markup.add(types.KeyboardButton("WebApp", web_app=WebAppInfo(url='https://vadimirozz.github.io/kinda.html')))
        photo = open('p.jpg', 'rb')
        await bot.send_photo(message.chat.id, photo, caption="🤗 С теплом приветствуем вас! Откройте двери в мир "
                                                             "изысканных вкусов и непередаваемых эмоций. Приятного время "
                                                             "провождения!", reply_markup=markup)

    @dp.message_handler(content_types=['web_app_data'])
    async def handle_message(message: types.Message):
        res = json.loads(message.web_app_data.data)
        await queue.put(res)


async def second_bot(token, queue, dp):
    bot = Bot(token)

    markup = InlineKeyboardMarkup(row_width=3)
    btn1 = InlineKeyboardButton('✅', callback_data='accept')
    btn2 = InlineKeyboardButton('❌', callback_data='cancel')
    btn3 = InlineKeyboardButton('🕔', callback_data='reschedule')
    markup.add(btn1, btn2, btn3)

    @dp.callback_query_handler(lambda c: c.data == 'accept')
    async def accept_callback(callback_query: CallbackQuery):
        await send_action(callback_query, "Заказ принят!")
        await callback_query.message.answer("Accept!")


    @dp.callback_query_handler(lambda c: c.data == 'cancel')
    async def cancel_callback(callback_query: CallbackQuery):
        await send_action(callback_query, "Заказ отменен!")
        await callback_query.message.answer("Cancel!")

    @dp.callback_query_handler(lambda c: c.data == 'reschedule')
    async def reschedule_callback(callback_query: CallbackQuery, state: FSMContext):
        await send_action(callback_query, "Выберите новое время для заказа:")
        async with state.proxy() as data:
            await state.set_state("newtime")
            data['user_id'] = callback_query.from_user.id


    @dp.message_handler(state="newtime")
    async def process_newtime(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['new_time'] = message.text
        await send_action(message, "Новое время выбрано: " + message.text)
        await state.finish()  # Завершаем состояние

    async def send_action(callback_query: CallbackQuery, action_text: str):
        await callback_query.answer()
        await callback_query.message.answer(action_text)

    async def send_action(entity, action_text: str):
        await entity.answer(action_text)

    while True:
        data = await queue.get()
        message_text = (
            f'Новый заказ!\n'
            f'Имя: {data["name"]}\n'
            f'Номер: {data["phone"]}\n'
            f'Email: {data["email"]}\n'
            f'Комментарий: {data["comment"]}\n'
            f'Время готовности заказа: {data["time"]}'
        )
        await bot.send_message(chat_id="1977381863", text=message_text, reply_markup=markup)

async def main():
    token1 = "6420992088:AAHxzOYNOz2BkrSEN5O7q-iaVfPtGrCViSQ"
    token2 = "6200911169:AAGXtE68S95fJpS5ijdJkqqslD32aW-G4zM"

    queue = asyncio.Queue()

    storage = MemoryStorage()

    bot1 = Bot(token1)
    dp1 = Dispatcher(bot1, storage=storage)

    bot2 = Bot(token2)
    dp2 = Dispatcher(bot2, storage=storage)

    # Запускаем первого бота
    asyncio.create_task(first_bot(token1, queue, dp1))
    # Запускаем второго бота
    asyncio.create_task(second_bot(token2, queue, dp2))

    await asyncio.gather(
        dp1.start_polling(),
        dp2.start_polling()
    )

if __name__ == "__main__":
    asyncio.run(main())
