from dataclasses import dataclass


@dataclass(slots=True)
class BotConfig:
    token: str
