import asyncio
import logging
import xml.etree.ElementTree as ET
from typing import NoReturn

import aiohttp
import backoff
from aiohttp import ClientTimeout
from exchange_rate_service.common.config_loader import load_config
from exchange_rate_service.common.storage import init_storage
from exchange_rate_service.updater.config import CBRConfig

logger = logging.getLogger(__name__)


@backoff.on_exception(
    backoff.expo,
    (aiohttp.ClientError, TimeoutError),
    max_time=300,
)
async def fetch_exchange_rates(url: str) -> str:
    async with (
        aiohttp.ClientSession(timeout=ClientTimeout(10)) as session,
        session.get(url) as resp,
    ):
        return await resp.text()


def parse_cbr_xml(xml: str) -> dict[str, str]:
    root = ET.ElementTree(ET.fromstring(xml)).getroot()

    exchange_rates_map = {}
    for child in root.findall("Valute"):
        code = child.find("CharCode").text
        value = child.find("VunitRate").text.replace(",", ".")

        exchange_rates_map[code] = value

    return exchange_rates_map


async def fetch_and_update() -> None:
    cbr_config = load_config(CBRConfig, scope="cbr")

    storage = init_storage()

    try:
        cbr_xml = await fetch_exchange_rates(url=cbr_config.url)
    except Exception:
        logger.exception("Couldn't get data")
    else:
        exchange_rates_map = parse_cbr_xml(cbr_xml)

        await storage.update(exchange_rates_map)

    await storage.close()


def main() -> NoReturn:
    asyncio.run(fetch_and_update())


if __name__ == "__main__":
    main()
