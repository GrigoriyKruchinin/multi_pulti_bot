import asyncio
import logging

from aiogram import Bot, Dispatcher

from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN
from routers import router


bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def main():
    """
    Основная функция запуска бота.
    Инициализирует логирование и запускает polling.
    """
    logging.basicConfig(level=logging.INFO)
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
