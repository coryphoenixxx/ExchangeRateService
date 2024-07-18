from dataclasses import dataclass


@dataclass(slots=True)
class CBRConfig:
    url: str
