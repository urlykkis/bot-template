import pytest

from aiogram import Dispatcher, Bot
from aiogram.methods import SendMessage
from fluentogram import TranslatorRunner

from tests.mocks.updates import get_update, get_message
from tests.mocks.aiogram_mocks.users import AiogramUser


@pytest.mark.usefixtures("cls_dp", "cls_bot", "cls_i18n")
class TestAdminMenu:
    """
    Тестирует tgbot/routers/admin/menu
    """
    bot: Bot
    dispatcher: Dispatcher
    i18n: TranslatorRunner

    @pytest.mark.asyncio
    async def test_admin_menu(self):
        """Тестирует /admin"""
        aiogram_user = AiogramUser()
        aiogram_user.user = aiogram_user._get_user(user_id=5604729322)
        aiogram_user.chat = aiogram_user._get_chat()

        message = get_message(
            self.bot,
            text="/admin",
            chat=aiogram_user.chat,
            from_user=aiogram_user.user
        )

        update = get_update(message=message)

        result: SendMessage = await self.dispatcher.feed_update(
            bot=self.bot, update=update,
        )

        assert isinstance(result, SendMessage)
        assert result.text == self.i18n.admin.menu()
