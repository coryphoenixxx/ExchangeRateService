import asyncio
from typing import NoReturn

from exchange_rate_service.common.config_loader import load_config
from exchange_rate_service.common.configs import CBRConfig
from exchange_rate_service.common.storage import init_storage
from exchange_rate_service.updater.fetch_and_update import fetch_and_update


async def main_loop() -> NoReturn:
    cbr_config = load_config(CBRConfig, scope="cbr")

    await fetch_and_update(
        url=cbr_config.url,
        storage=init_storage(),
    )

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    asyncio.run(main_loop())
