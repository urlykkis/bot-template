import pytest

from contextlib import nullcontext as does_not_raise

from aiogram import Dispatcher, Bot
from aiogram.types import ChatMemberLeft, ChatMemberMember
from fluentogram import TranslatorRunner

from src.domain.channel.dto.channel import ChannelDTO
from src.domain.channel.exceptions.channel import ChannelNotExists

from tests.mocks.updates import get_update, get_chat_member_updated
from tests.mocks.aiogram_mocks.users import AiogramUser
from tests.utils.asserts.channel import assert_channel


@pytest.mark.usefixtures("cls_dp", "cls_bot", "cls_i18n")
class TestChannelActive:
    """
    Тестирует tgbot/routers/channel/active
    Бота добавляют в канал/удаляют из канала
    """
    bot: Bot
    dispatcher: Dispatcher
    i18n: TranslatorRunner

    async def update_add_channel(self, aiogram_user):
        chat_member_updated = get_chat_member_updated(
            chat=aiogram_user.chat,
            user=aiogram_user.user,
            old_chat_member=ChatMemberLeft(user=aiogram_user.user),
            new_chat_member=ChatMemberMember(user=aiogram_user.user),
        )

        result: ChannelDTO = await self.dispatcher.feed_update(
            bot=self.bot, update=get_update(my_chat_member=chat_member_updated),
        )
        return result

    @pytest.mark.asyncio
    async def test_channel_add_handler(self):
        aiogram_user = AiogramUser()
        aiogram_user.chat = aiogram_user._get_chat(type="channel")

        result = await self.update_add_channel(aiogram_user)

        assert isinstance(result, ChannelDTO)
        assert result is not None
        assert_channel(result)

        assert result.chat_id == aiogram_user.chat.id

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ('create', 'expect'),
        [
            (False, pytest.raises(ChannelNotExists)),
            (True, does_not_raise())
        ]
    )
    async def test_channel_delete_handler(
            self, create, expect
    ):
        with expect:
            aiogram_user = AiogramUser()
            aiogram_user.chat = aiogram_user._get_chat(chat_id=777, type="channel")

            if create is True:
                await self.update_add_channel(aiogram_user)

            chat_member_updated = get_chat_member_updated(
                chat=aiogram_user.chat,
                user=aiogram_user.user,
                old_chat_member=ChatMemberMember(user=aiogram_user.user),
                new_chat_member=ChatMemberLeft(user=aiogram_user.user),
            )

            result: bool = await self.dispatcher.feed_update(
                bot=self.bot, update=get_update(my_chat_member=chat_member_updated),
            )

            assert isinstance(result, bool)
            assert result == create
