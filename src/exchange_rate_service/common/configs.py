from dataclasses import dataclass


@dataclass(slots=True)
class BotConfig:
    token: str


@dataclass(slots=True)
class StorageConfig:
    hm_name: str
    base_currency: str
    redis_host: str
    redis_port: int
    redis_password: str


@dataclass(slots=True)
class CBRConfig:
    url: str
