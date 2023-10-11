import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from bot.start_router import start_router
from bot.main_router import main_router

import config

logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s :: %(asctime)s :: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def main() -> None:
    dp = Dispatcher()
    dp.include_routers(
        start_router,
        main_router,
    )

    bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

try:
    logger.info("Polling started")

    asyncio.run(main())

    logger.info("Polling stopped manually")
except Exception as e:
    logger.error('Error while polling: {}'.format(e))
