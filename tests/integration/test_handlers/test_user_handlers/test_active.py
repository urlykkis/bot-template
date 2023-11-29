import pytest

from aiogram import Dispatcher, Bot
from aiogram.types import ChatMemberLeft, ChatMemberMember
from fluentogram import TranslatorRunner

from src.domain.user.usecase.user import UserService
from src.domain.user.dto.user import UserDTO

from tests.mocks.updates import get_update, get_chat_member_updated
from tests.mocks.aiogram_mocks.users import AiogramUser
from tests.utils.asserts.user import assert_user


@pytest.mark.usefixtures("cls_dp", "cls_bot", "cls_i18n")
class TestActive:
    """
    Тестирует tgbot/routers/user/active
    Пользователь блокирует/разблокирует бота
    """
    bot: Bot
    dispatcher: Dispatcher
    i18n: TranslatorRunner

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("chat_member", "expected"),
        [
            ([ChatMemberLeft, ChatMemberMember], True),
            ([ChatMemberMember, ChatMemberLeft], False),
        ]
    )
    async def test_active_true_handler(
            self, user_service: UserService,
            chat_member, expected
    ):
        aiogram_user = AiogramUser()

        chat_member_updated = get_chat_member_updated(
            chat=aiogram_user.chat,
            user=aiogram_user.user,
            old_chat_member=chat_member[0](user=aiogram_user.user),
            new_chat_member=chat_member[1](user=aiogram_user.user),
        )

        result: UserDTO = await self.dispatcher.feed_update(
            bot=self.bot, update=get_update(my_chat_member=chat_member_updated),
        )

        assert isinstance(result, UserDTO)
        assert result is not None
        assert_user(result)
        assert result.active is expected
