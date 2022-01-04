import asyncio
import logging

from config.bot_config import token

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.handlers.choose_universities import register_select_vuz_func
from app.handlers.begining import register_begining

logger = logging.getLogger(__name__)

# предложение выбора команд на выбор
async def set_commands(bot: Bot):
    command = [
        BotCommand(command='/start', description='Начало работы'),
        BotCommand(command='/finish', description='Конец выбора ВУЗов'),
        # BotCommand(command='', description=''),
    ]

async def main():
    # настройка логировния (чего происходит в программе)
    logging.basicConfig(
        level= logging.INFO,
        format= '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    )
    logger.error('Bot starts work.')

    # инициализация бота и диспетчера
    bot = Bot(token= token)
    dp = Dispatcher(bot, storage= MemoryStorage)

    # регистриация обработчиков
    register_select_vuz_func(dp)
    register_begining(dp)

    # установка команд
    await set_commands(bot)

    # начало работы
    await dp.skip_updates()
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())