import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode

from callbacks import setup_callback_routers
from config import config
from handlers import setup_message_routers
from middlewares import ThrottlingMiddleware

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    bot = Bot(config.BOT_TOKEN.get_secret_value(), parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    dp.message.middleware(ThrottlingMiddleware())

    message_routers = setup_message_routers()
    callback_routers = setup_callback_routers()
    dp.include_router(message_routers)
    dp.include_router(callback_routers)

    await bot.delete_webhook(True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
