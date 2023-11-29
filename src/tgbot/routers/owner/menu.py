from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


router = Router(name="owner_menu")


@router.message(Command("owner"))
async def owner_handler(message: Message):
    return await message.answer("Owner")
