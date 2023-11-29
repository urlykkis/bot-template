import pytest

from src.infrastructure.database.uow.alchemy.uow import SQLAlchemyUoW
from src.infrastructure.database.repositories.user import UserRepository
from src.infrastructure.database.repositories.chat import ChatRepository
from src.infrastructure.database.repositories.channel import ChannelRepository

from src.domain.user.usecase.user import UserService
from src.domain.chat.usecase.chat import ChatService
from src.domain.channel.usecase.channel import ChannelService



@pytest.fixture(scope="session")
def uow(db_session):
    return SQLAlchemyUoW(
        session=db_session,
        user_repo=UserRepository,
        chat_repo=ChatRepository,
        channel_repo=ChannelRepository
    )


@pytest.fixture
def user_service(uow):
    return UserService(uow=uow)


@pytest.fixture
def chat_service(uow):
    return ChatService(uow=uow)


@pytest.fixture
def channel_service(uow):
    return ChannelService(uow=uow)
