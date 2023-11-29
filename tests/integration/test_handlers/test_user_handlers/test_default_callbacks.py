import pytest

from aiogram import Dispatcher, Bot
from fluentogram import TranslatorRunner

from tests.mocks.updates import \
    get_message, get_update,\
    get_callback_query
from tests.mocks.aiogram_mocks.users import AiogramUser


@pytest.mark.usefixtures("cls_dp", "cls_bot", "cls_i18n")
class TestDefaultCallback:
    """
    Тестирует обычные callback (hide, cancel)
    """
    bot: Bot
    dispatcher: Dispatcher
    i18n: TranslatorRunner

    @pytest.mark.asyncio
    async def test_hide_callback(self):
        """тестирует call.data == hide"""
        aiogram_user = AiogramUser()

        message = get_message(
            self.bot,
            text="msg",
            chat=aiogram_user.chat,
            from_user=aiogram_user.user
        )
        callback = get_callback_query(
            self.bot,
            data="hide",
            user=aiogram_user.user,
            message=message
        )

        result: bool = await self.dispatcher.feed_update(
            bot=self.bot, update=get_update(callback_query=callback),
        )

        assert isinstance(result, bool)

    @pytest.mark.asyncio
    async def test_cancel_callback(self):
        """тестирует call.data == cancel"""
        aiogram_user = AiogramUser()

        message = get_message(
            self.bot,
            text="msg",
            chat=aiogram_user.chat,
            from_user=aiogram_user.user
        )
        state = self.dispatcher.fsm.get_context(
            self.bot,
            chat_id=message.chat.id,
            user_id=message.from_user.id,
        )
        await state.set_state("asd")

        callback = get_callback_query(
            self.bot,
            data="cancel",
            user=aiogram_user.user,
            message=message,
            state=state
        )

        result: bool = await self.dispatcher.feed_update(
            bot=self.bot,
            update=get_update(callback_query=callback, state=state),
            state=state
        )

        assert isinstance(result, bool)
        assert await state.get_state() is None
