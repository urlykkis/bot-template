from src.domain.channel.interfaces.persistence import IChannelRepo
from src.domain.base.interfaces.uow import IUoW


class IChannelUoW(IUoW):
    """Интерфейс Unit of Work для работы с канала"""
    channel: IChannelRepo
