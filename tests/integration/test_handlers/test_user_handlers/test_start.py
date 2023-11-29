import pytest

from aiogram import Dispatcher, Bot
from aiogram.types import Message
from aiogram.methods import SendMessage
from fluentogram import TranslatorRunner

from src.domain.user.usecase.user import UserService
from src.domain.user.dto.user import UserDTO

from tests.mocks.updates import get_message, get_update
from tests.mocks.aiogram_mocks.users import AiogramUser
from tests.utils.asserts.user import assert_user


@pytest.mark.usefixtures("cls_dp", "cls_bot", "cls_i18n")
class TestStart:
    """
    Тестирует tgbot/routers/user/start
    """
    bot: Bot
    dispatcher: Dispatcher
    i18n: TranslatorRunner

    @pytest.mark.asyncio
    async def test_start(self, user_service: UserService):
        """Тестирует команду /start"""
        aiogram_user = AiogramUser()

        message: Message = get_message(
            self.bot, "/start",
            from_user=aiogram_user.user,
            chat=aiogram_user.chat
        )

        result: SendMessage = await self.dispatcher.feed_update(
            bot=self.bot, update=get_update(message=message),
        )

        assert isinstance(result, SendMessage)
        assert result.text == self.i18n.user.start()

        user: UserDTO = await user_service.get_user(user_id=message.from_user.id)

        assert user is not None
        assert_user(user)
