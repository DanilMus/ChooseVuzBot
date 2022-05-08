import asyncio
import logging

from config.bot_config import token

from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.handlers.introduction import register_introduction
from app.handlers.choose_universities import register_choose_vuz
from app.handlers.choose_subjects import register_choose_subjects
from app.handlers.choose_prioritets_for_criteria import register_prioritets_for_criteria
from app.handlers.choose_top import register_top
from app.handlers.show_rating import register_show_rating
from app.handlers.the_end import register_the_end

from app.handlers.admin import register_admin


logger = logging.getLogger(__name__)

# предложение выбора команд на выбор
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command= '/start', description= 'Начало работы'),
        BotCommand(command= '/finish1', description= 'Конец выбора ВУЗов'),
        BotCommand(command= '/finish2', description= 'Конец выбора предметов'),
        BotCommand(command= '/all', description= 'Выбираем все ВУЗы'),
    ]
    await bot.set_my_commands(commands)


async def main():
    # настройка логировния (чего происходит в программе)
    logging.basicConfig(
        level= logging.INFO,
        format= '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    )
    logger.error('Bot starts work.')

    # инициализация бота и диспетчера
    bot = Bot(token= token, parse_mode= types.ParseMode.HTML)
    dp = Dispatcher(bot, storage= MemoryStorage())

    # регистриация обработчиков
    register_admin(dp)
    
    register_introduction(dp)
    register_choose_vuz(dp)
    register_choose_subjects(dp)
    register_prioritets_for_criteria(dp)
    register_top(dp)
    register_show_rating(dp)
    register_the_end(dp)


    # установка команд
    await set_commands(bot)

    # начало работы
    # await dp.skip_updates() # потом надо будет убрать 
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())