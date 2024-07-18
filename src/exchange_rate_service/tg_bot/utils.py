from collections.abc import Generator, Sequence
from typing import TypeVar

T = TypeVar("T")


def chunked(seq: Sequence["T"], n: int) -> Generator[list["T"], None, None]:
    for i in range(0, len(seq), n):
        yield seq[i : i + n]


def build_codes_matrix(codes_list: list[str]) -> str:
    matrix = ""

    for row in chunked(codes_list, 5):
        for code in row:
            matrix += code + ", "
        matrix += "\n"

    return matrix[:-3]
