from exchange_rate_service.common.config_loader import load_config
from exchange_rate_service.common.configs import StorageConfig
from redis import asyncio as redis


class CurrencyCodeNotExistsError(Exception):
    def __init__(self, code: str) -> None:
        super().__init__()
        self.code = code


class RatesStorage:
    def __init__(self, hm_name: str, base_currency: str, **kwargs) -> None:
        self._hm_name = hm_name
        self._r = redis.Redis(**kwargs)
        self._base_currency = base_currency

    async def update(self, exchange_rates_map: dict[str, str]) -> None:
        await self._r.hset(name=self._hm_name, mapping=exchange_rates_map)

    async def get_by_codes(self, codes: tuple[str, ...]) -> dict[str, float]:
        raw_values = await self._r.hmget(name=self._hm_name, keys=list(codes))

        result = {}
        for k, v in zip(codes, raw_values, strict=False):
            if k == self._base_currency:
                result[k] = 1.0
            elif v is None:
                raise CurrencyCodeNotExistsError(code=k)
            else:
                result[k] = float(v)

        return result

    async def get_all_codes(self) -> tuple[str, ...]:
        raw = await self._r.hkeys(name=self._hm_name)

        return tuple([v.decode() for v in raw])

    async def get_rates(self) -> dict[str, float]:
        raw = await self._r.hgetall(name=self._hm_name)

        return {k.decode(): float(v) for k, v in raw.items()}

    async def close(self) -> None:
        await self._r.aclose()


def init_storage() -> RatesStorage:
    config = load_config(StorageConfig, scope="storage")

    return RatesStorage(
        hm_name=config.hm_name,
        base_currency=config.base_currency,
        host=config.redis_host,
        port=config.redis_port,
        password=config.redis_password,
    )
