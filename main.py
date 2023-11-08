import logging
from aiogram import Dispatcher, types, Bot, executor
from config import TOKEN
from buttons import home
from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, parse_mode="html")
dp = Dispatcher(bot, storage=MemoryStorage())


value = ''
value2 = ''

@dp.message_handler(commands=["start"], state='*')
async def start_page(message: types.Message):
    await message.answer_photo(photo='https://phonoteka.org/uploads/posts/2021-05/1620079468_26-phonoteka_org-p-kalkulyator-fon-30.jpg', caption=f"0", reply_markup=home)

@dp.callback_query_handler()
async def math_func(query):
    global value, value2
    data = query.data

    if data == 'no':
        pass
    elif data == 'del':
        value = ''
    elif data == '<=':
        if value != '':
            value = value[:len(value)-1]
    elif data == '=':
        try:
            value = str(eval(value))
        except:
            value = "⛔️ Tizimda xatolik!"
    else:
        value += data
    if (value != value2 and value != '') or ('0' != value2 and value == ''):
        if value == '':
            await bot.edit_message_caption(chat_id=query.message.chat.id, message_id=query.message.message_id, caption='0', reply_markup=home)
        else:
            await bot.edit_message_caption(chat_id=query.message.chat.id, message_id=query.message.message_id, caption=value, reply_markup=home)
    value2 = value

    if value == '⛔️ Tizimda xatolik!':
        value = ''

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
