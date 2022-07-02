# базовые настройки
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config.bot_config import token

# обработчики
from app.handlers.start import register_start


logger = logging.getLogger(__name__)
async def main():
    # настройка логирования
    logging.basicConfig(
        level= logging.INFO,
        format= '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    )
    logger.info('Bot starts work')

    # иннициализация бота
    bot = Bot(token= token, parse_mode= types.ParseMode.HTML)
    dp = Dispatcher(bot) #, storage= MemoryStorage)

    # установка команд
    commands = []
    await bot.set_my_commands(commands)


    # регистрация обработчиков
    await register_start(dp)

    # начало работы
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())