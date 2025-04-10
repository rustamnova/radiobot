import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
print(f"TOKEN: {TOKEN}")  # ← добавь эту строку



# Список радиостанций
RADIO_CHANNELS = {
    "Radio Record": "https://radiorecord.hostingradio.ru/rr_main96.aacp",
    "Relax FM": "http://ic7.101.ru:8000/v12_1",
    "Europa Plus": "http://ep256.hostingradio.ru:8052/europaplus256.mp3",
    "Ретро FM": "http://retroserver.streamr.ru:8043/retro256.mp3"
}

# Клавиатура
def radio_keyboard():
    kb = InlineKeyboardBuilder()
    for name in RADIO_CHANNELS.keys():
        kb.button(text=name, callback_data=name)
    kb.adjust(1)
    return kb.as_markup()

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(F.text == "/start")
async def start_handler(message: Message):
    await message.answer(
        "🎧 Выберите радиостанцию для прослушивания:",
        reply_markup=radio_keyboard()
    )

@dp.callback_query()
async def radio_callback(callback: types.CallbackQuery):
    station = callback.data
    stream_url = RADIO_CHANNELS.get(station)
    if stream_url:
        await callback.message.answer(
            f"📡 <b>{station}</b>\nНажмите на ссылку ниже, чтобы начать прослушивание:\n{stream_url}",
            parse_mode=ParseMode.HTML
        )
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
