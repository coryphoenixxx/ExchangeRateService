import os
from pathlib import Path
from typing import TypeVar

import tomllib
from adaptix import Retort

T = TypeVar("T")


class ConfigNotFoundError(Exception): ...


def load_config(
    typ: type[T],
    scope: str | None = None,
) -> T:
    path = os.getenv("CONFIG_PATH")

    if path is None:
        raise ConfigNotFoundError

    with Path(path).open("rb") as f:
        data = tomllib.load(f)

    if scope is not None:
        data = data[scope]

    dcf = Retort()

    return dcf.load(data, typ)
