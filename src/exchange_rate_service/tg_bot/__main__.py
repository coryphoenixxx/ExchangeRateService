import asyncio
import logging
import sys
from functools import partial

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from exchange_rate_service.common.config_loader import load_config
from exchange_rate_service.common.configs import BotConfig
from exchange_rate_service.common.converter import Converter
from exchange_rate_service.common.storage import RatesStorage, init_storage
from exchange_rate_service.tg_bot.contollers import router

logger = logging.getLogger(__name__)


async def on_startup() -> None:
    logger.info("Bot successfully started.")


async def on_shutdown(bot: Bot, storage: RatesStorage) -> None:
    logger.info("Bot is stopping...")
    await bot.session.close()
    await storage.close()


async def polling_run(bot: Bot, dp: Dispatcher) -> None:
    await dp.start_polling(bot)


def main() -> None:
    bot_config = load_config(BotConfig, scope="bot")

    bot = Bot(
        token=bot_config.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()

    storage = init_storage()

    dp["storage"] = storage
    dp["converter"] = Converter(storage=storage)

    dp.include_router(router)

    dp.shutdown.register(on_startup)
    dp.startup.register(partial(on_shutdown, storage=storage))

    asyncio.run(polling_run(bot, dp))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
