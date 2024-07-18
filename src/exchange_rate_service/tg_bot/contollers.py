from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import Message
from exchange_rate_service.common.converter import (
    Converter,
    NegativeUnitCountError,
    SuperBigUnitValueError,
)
from exchange_rate_service.common.storage import (
    CurrencyCodeNotExistsError,
    RatesStorage,
)
from exchange_rate_service.tg_bot.utils import build_codes_matrix

router = Router()


@router.message(CommandStart())
async def start_handler(msg: Message) -> None:
    await msg.answer("Hi!")


@router.message(Command("exchange"))
async def exchange_handler(
    msg: Message,
    command: CommandObject,
    *,
    storage: RatesStorage,
    converter: Converter,
) -> None:
    try:
        code_from, code_to, units = command.args.split(" ")
        units = float(units)
    except (ValueError, AttributeError):
        await msg.answer(
            "INVALID INPUT.\n\n Use <code>{CODE_FROM} {CODE_TO} {NUMBER}</code> format.",
            parse_mode=ParseMode.HTML,
        )
    else:
        try:
            result = await converter.convert(code_from, code_to, units)
        except CurrencyCodeNotExistsError as err:
            codes_list = await storage.get_all_codes()
            codes_list_repr = build_codes_matrix(list(codes_list))

            await msg.answer(
                text=(
                    f"INVALID CURRENCY CODE: <b>{err.code}</b>\n\n<u>"
                    f"Use next:</u>\n<code>{codes_list_repr}</code>"
                )
            )
        except NegativeUnitCountError:
            await msg.answer("INVALID INPUT. Value must be positive.")
        except SuperBigUnitValueError:
            await msg.answer("INVALID INPUT. Reduce the value.")
        else:
            await msg.answer(text=f"RESULT: <b>{result}</b>")


@router.message(Command("rates"))
async def rates_handler(
    msg: Message,
    *,
    storage: RatesStorage,
) -> None:
    rates = await storage.get_rates()

    rates_text = "\n".join([f"<b>{k} -- {v}</b>" for k, v in rates.items()])

    await msg.answer(text=f"<code>{rates_text}</code>", parse_mode=ParseMode.HTML)
