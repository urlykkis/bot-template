import pytest

from aiogram import Dispatcher, Bot
from aiogram.methods import SendMessage
from fluentogram import TranslatorRunner

from tests.mocks.updates import get_update, get_message
from tests.mocks.aiogram_mocks.users import AiogramUser


@pytest.mark.usefixtures("cls_dp", "cls_bot", "cls_i18n")
class TestOwnerMenu:
    """
    Тестирует tgbot/routers/owner/menu
    """
    bot: Bot
    dispatcher: Dispatcher
    i18n: TranslatorRunner

    @pytest.mark.asyncio
    async def test_owner_menu(self):
        """Тестирует /owner"""
        aiogram_user = AiogramUser()
        aiogram_user.user = aiogram_user._get_user(user_id=1046227957)
        aiogram_user.chat = aiogram_user._get_chat()

        message = get_message(
            self.bot,
            text="/owner",
            chat=aiogram_user.chat,
            from_user=aiogram_user.user
        )

        update = get_update(message=message)

        result: SendMessage = await self.dispatcher.feed_update(
            bot=self.bot, update=update,
        )

        assert isinstance(result, SendMessage)
        assert result.text == "Owner"
