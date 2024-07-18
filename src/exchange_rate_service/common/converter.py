from decimal import ROUND_HALF_EVEN, Decimal, InvalidOperation

from exchange_rate_service.common.storage import RatesStorage


class NegativeUnitCountError(Exception): ...


class SuperBigUnitValueError(Exception): ...


class Converter:
    def __init__(self, storage: RatesStorage) -> None:
        self._storage = storage

    async def convert(
        self,
        code_from: str,
        code_to: str,
        units: float,
    ) -> Decimal:
        if units < 0:
            raise NegativeUnitCountError

        result = await self._storage.get_by_codes(codes=(code_from, code_to))
        value_from, value_to = result[code_from], result[code_to]

        result = Decimal(units) * Decimal(value_from) / Decimal(value_to)

        try:
            rounded = result.quantize(Decimal(".001"), rounding=ROUND_HALF_EVEN)
        except InvalidOperation as err:
            raise SuperBigUnitValueError from err

        return rounded
