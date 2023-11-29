import pytest

from contextlib import nullcontext as does_not_raise

from aiogram import Dispatcher, Bot
from aiogram.types import ChatMemberLeft, ChatMemberMember
from fluentogram import TranslatorRunner

from src.domain.chat.dto.chat import ChatDTO
from src.domain.chat.exceptions.chat import ChatNotExists

from tests.mocks.updates import get_update, get_chat_member_updated, get_message
from tests.mocks.aiogram_mocks.users import AiogramUser
from tests.utils.asserts.chat import assert_chat


@pytest.mark.usefixtures("cls_dp", "cls_bot", "cls_i18n")
class TestChatActive:
    """
    Тестирует tgbot/routers/chat/active
    Бота добавляют в группу/удаляют из группы
    Группа мигрируется в супергруппу
    """
    bot: Bot
    dispatcher: Dispatcher
    i18n: TranslatorRunner

    async def update_add_group(self, aiogram_user):
        chat_member_updated = get_chat_member_updated(
            chat=aiogram_user.chat,
            user=aiogram_user.user,
            old_chat_member=ChatMemberLeft(user=aiogram_user.user),
            new_chat_member=ChatMemberMember(user=aiogram_user.user),
        )

        result: ChatDTO = await self.dispatcher.feed_update(
            bot=self.bot, update=get_update(my_chat_member=chat_member_updated),
        )
        return result

    @pytest.mark.asyncio
    async def test_chat_add_handler(self):
        aiogram_user = AiogramUser()
        aiogram_user.chat = aiogram_user._get_chat(type="group")

        result = await self.update_add_group(aiogram_user)

        assert isinstance(result, ChatDTO)
        assert result is not None
        assert_chat(result)

        assert result.chat_id == aiogram_user.chat.id

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ('create', 'expect'),
        [
            (False, pytest.raises(ChatNotExists)),
            (True, does_not_raise())
        ]
    )
    async def test_chat_delete_handler(
            self, create, expect
    ):
        with expect:
            aiogram_user = AiogramUser()
            aiogram_user.chat = aiogram_user._get_chat(chat_id=777, type="group")

            if create is True:
                await self.update_add_group(aiogram_user)

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

    @pytest.mark.asyncio
    @pytest.mark.skip
    @pytest.mark.parametrize(
        ("new_chat_id", "create", "expect"),
        [
            # (0, True, does_not_raise()),
            (1, False, pytest.raises(ChatNotExists)),
        ]
    )
    async def test_migrate_chat(
            self,
            new_chat_id, create, expect
    ):
        """Не отлавливается"""
        with expect:
            aiogram_user = AiogramUser()
            aiogram_user.chat = aiogram_user._get_chat(type="group")
            message = get_message(
                self.bot,
                text=None,
                chat=aiogram_user.chat,
                from_user=aiogram_user.user,
                migrate_to_chat_id=new_chat_id,
                migrate_from_chat_id=aiogram_user.chat.id
            )

            if create is True:
                await self.update_add_group(aiogram_user)

            result: ChatDTO = await self.dispatcher.feed_update(
                bot=self.bot, update=get_update(message=message),
            )

            assert isinstance(result, ChatDTO)
            assert_chat(result)

            assert result.chat_id == new_chat_id
