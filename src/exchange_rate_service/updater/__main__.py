import asyncio
from typing import NoReturn

from exchange_rate_service.updater.fetch_and_update import fetch_and_update


async def main_loop() -> NoReturn:
    await fetch_and_update()

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    asyncio.run(main_loop())
