import asyncio

from aiogram import Bot, Dispatcher, types , Router 
from aiogram.filters.command import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.methods import DeleteWebhook
from aiogram.types import Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionMiddleware

import logging
import os

from database.database import DB
from handlers import adm_hand, user_hand
from configs import TOKEN

# load_dotenv()


async def on_startup(_):
    with DB() as db :
        db.create_tables()


bot_ = Bot(token=TOKEN, parse_mode='HTML')


logging.basicConfig(level=logging.INFO)

# Включаем логирование, чтобы не пропустить важные сообщения
async def main():
    # Объект бота
    bot = bot_
    storage = MemoryStorage()
    # Диспетчер
    dp = Dispatcher(storage=storage)
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_routers(adm_hand.router, user_hand.router)

    await dp.start_polling(bot, on_startup=on_startup)
    

# Запуск процесса поллинга новых апдейтов


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')