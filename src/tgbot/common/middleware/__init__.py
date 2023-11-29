from aiogram import Dispatcher, Bot, F
from aiogram.utils.chat_action import ChatActionMiddleware
from sqlalchemy.orm import sessionmaker


from .outer import \
    DatabaseMiddleware, ServicesMiddleware, \
    LoggingMiddleware, ManagerMiddleware
from .inner import \
    TranslatorRunnerMiddleware, UserMiddleware, \
    ThrottlingMiddleware, GlobalTimeoutMiddleware


def setup_middleware(dp: Dispatcher, sm: sessionmaker, ignore_throttling: bool = False):
    dp.update.outer_middleware(LoggingMiddleware())
    dp.update.outer_middleware(ManagerMiddleware())
    dp.update.outer_middleware(DatabaseMiddleware(sm))
    dp.update.outer_middleware(ServicesMiddleware())
    dp.update.middleware(TranslatorRunnerMiddleware())

    dp.message.filter(F.chat.type.in_({"private"}))
    dp.update.middleware(UserMiddleware())

    if ignore_throttling is False:
        dp.message.middleware(ThrottlingMiddleware())
        dp.callback_query.middleware(ThrottlingMiddleware())

    dp.message.middleware(GlobalTimeoutMiddleware())
    dp.message.middleware(ChatActionMiddleware())
