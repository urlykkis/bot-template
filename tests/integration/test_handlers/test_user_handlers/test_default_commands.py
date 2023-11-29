import pytest

from aiogram import Dispatcher, Bot
from aiogram.methods import SendMessage
from fluentogram import TranslatorRunner

from tests.mocks.updates import get_message, get_update
from tests.mocks.aiogram_mocks.users import AiogramUser


@pytest.mark.usefixtures("cls_dp", "cls_bot", "cls_i18n")
class TestDefaultCommands:
    """
    Тестирует обычные команды (/settings, /help)
    """
    bot: Bot
    dispatcher: Dispatcher
    i18n: TranslatorRunner

    @pytest.mark.asyncio
    async def test_settings_command(self):
        """Тестирует команду /settings"""
        aiogram_user = AiogramUser()

        message = get_message(
            self.bot,
            text="/settings",
            chat=aiogram_user.chat,
            from_user=aiogram_user.user
        )

        result: SendMessage = await self.dispatcher.feed_update(
            bot=self.bot, update=get_update(message=message),
        )

        assert isinstance(result, SendMessage)
        assert result is not None
        assert result.text == self.i18n.user.settings()

    @pytest.mark.asyncio
    async def test_help_command(self):
        """Тестирует команду /help"""
        aiogram_user = AiogramUser()

        message = get_message(
            self.bot,
            text="/help",
            chat=aiogram_user.chat,
            from_user=aiogram_user.user
        )

        result: SendMessage = await self.dispatcher.feed_update(
            bot=self.bot, update=get_update(message=message),
        )

        assert isinstance(result, SendMessage)
        assert result is not None
        assert result.text == self.i18n.user.help()
