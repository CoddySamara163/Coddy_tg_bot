import sys
import asyncio
import logging

from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

sys.path.append(str(Path(__file__).parent.parent))

from src.routers import router
from src.settings import settings


async def main() -> None:
    dp = Dispatcher()
    dp.include_router(router=router)

    logging.basicConfig(level=logging.INFO)
    bot = Bot(
        token=settings.TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await bot.delete_webhook()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
