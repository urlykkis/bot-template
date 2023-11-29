from contextlib import suppress

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from fluentogram import TranslatorRunner

router = Router(name="user_cancel")


@router.callback_query(F.data == "cancel")
async def cancel_handler(
        call: CallbackQuery,
        state: FSMContext,
        i18n: TranslatorRunner,
):
    """Отменяет текущее действие (state)"""
    with suppress(Exception):
        await state.clear()
        await call.message.delete()
        await call.message.answer(i18n.default.cancel())

    return True
