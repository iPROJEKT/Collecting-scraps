import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.utils.token import TokenValidationError
from dotenv import load_dotenv

from bot.handlers import (
    start_menu_handlers,
    robot_handler,
    change_robot_handler,
    defect_handler, observations
)
from bot.core.const import (
    LOG_FORM,
    LOG_FILEMOD,
    LOG_FILENAME,
    TOKEN_EXECT
)

load_dotenv()

logger = logging.getLogger(__name__)


async def main() -> None:
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    dp.include_routers(
        start_menu_handlers.router,
        robot_handler.router,
        change_robot_handler.router,
        defect_handler.router,
        observations.router
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(
        format=LOG_FORM,
        filemode=LOG_FILEMOD,
        filename=LOG_FILENAME,
        level=logging.INFO,
    )
    try:
        asyncio.run(main())
    except TokenValidationError:
        raise TokenValidationError(TOKEN_EXECT)
