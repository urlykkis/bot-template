from random import randint, choice
from string import ascii_lowercase, ascii_uppercase, digits

from aiogram.types import Chat, User


def random_string(start: int = 0, end: int = 40):
    """Возвращает строку с рандомными буквами"""
    symbols = ascii_uppercase + ascii_lowercase + digits
    return "".join([choice(symbols) for _ in range(start, end)])


class AiogramUser:
    """Mock объект пользователя Aiogram"""
    def __init__(self):
        self.user: User = self._get_user()
        self.chat: Chat = self._get_chat()

    def _get_user(
            self,
            user_id: int = randint(0, 99999999),
            first_name: str = random_string(),
            last_name: str | None = random_string(),
            username: str | None = random_string(end=32),
            language_code: str = "ru",
            is_premium: bool = True,
    ) -> User:
        """Возвращает объект пользователя"""
        return User(
            id=user_id,
            is_bot=False,
            first_name=first_name,
            last_name=last_name,
            username=username,
            language_code=language_code,
            is_premium=is_premium,
            added_to_attachment_menu=None,
            can_join_groups=None,
            can_read_all_group_messages=None,
            supports_inline_queries=None
        )

    def _get_chat(self, user: User | None = None, type: str = 'private', chat_id: int | None = None) -> Chat:
        """Возвращает объект чата"""
        self.user = user if user is not None else self.user

        return Chat(
            id=chat_id or self.user.id,
            type=type,
            title="321",
            username=self.user.username,
            first_name=self.user.first_name,
            last_name=self.user.last_name,
            photo=None,
            bio=None,
            has_private_forwards=None,
            join_to_send_messages=None,
            join_by_request=None,
            description=None,
            invite_link=None,
            pinned_message=None,
            permissions=None,
            slow_mode_delay=None,
            message_auto_delete_time=None,
            has_protected_content=None,
            sticker_set_name=None,
            can_set_sticker_set=None,
            linked_chat_id=None,
            location=None,
        )
