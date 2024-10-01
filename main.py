import asyncio
import logging
import os

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from routers import router as main_router
from sqlite import db_start
from handlers.parser import check_coin_balance

def on_startup():
    db_start()

#Получение логов от бота и делаем его непрерывным
async def main():
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(main_router)

    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    bot = Bot(
        #Токен бота
        token=os.getenv('TOKEN'),
        #Установка парс мода по умолчанию
        #default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML,
    ))
    on_startup()
    asyncio.create_task(check_coin_balance(bot))
    await dp.start_polling(bot)

#Запуск бота
if __name__ == "__main__":
    asyncio.run(main())