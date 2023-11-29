from typing import TypedDict, Any

from aiogram import types as tg, Bot, Router
from aiogram.dispatcher.event.handler import HandlerObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import BaseStorage
from aiogram.utils.callback_answer import CallbackAnswer

from fluentogram import TranslatorRunner, TranslatorHub

from src.infrastructure.settings.config import Config
from src.infrastructure.database.uow.alchemy.interface import SQLAlchemyIUoW
from src.domain.user.usecase.user import UserService
from src.domain.chat.usecase.chat import ChatService
from src.domain.channel.usecase.channel import ChannelService
from src.domain.user.dto.user import UserDTO


class AiogramMiddlewareData(TypedDict, total=False):
    event_from_user: tg.User
    event_chat: tg.Chat
    bot: Bot
    fsm_storage: BaseStorage
    state: FSMContext
    raw_state: Any
    handler: HandlerObject
    event_update: tg.Update
    event_router: Router
    callback_answer: CallbackAnswer
    translator_hub: TranslatorHub


class MiddlewareData(AiogramMiddlewareData, total=False):
    config: Config
    user: UserDTO | None
    uow: SQLAlchemyIUoW

    user_service: UserService
    chat_service: ChatService
    channel_service: ChannelService

    i18n: TranslatorRunner
