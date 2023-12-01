import os

from contextlib import suppress

from sqlalchemy import text
from aiogram import Bot
from aiogram.types import InputMediaDocument
from aiogram.exceptions import TelegramBadRequest

from src.infrastructure.settings import Config


async def backup_users(sm):
    """Создает файл с SQL-запросами для бэкапа таблицы user"""
    async with sm() as session:
        query = await session.execute(text("select * from users"))

        with open('./backup_users.sql', 'w', encoding="utf-8") as file:
            for row in query:
                try:
                    f.write(f"insert into users values ({row});\n")
                except Exception as e:
                    print('Error %s' % e)

        return "./backup_users.sql"


async def send_backup_files(bot: Bot, config: Config, paths):
    """Отправляет бэкап владельцу"""
    medias = [InputMediaDocument(media=path) for path in paths]
    medias[0].caption = "<b>⏳ Бэкап файлов</b>"

    with suppress(TelegramBadRequest):
        await bot.send_media_group(config.owner_id, medias)


async def auto_backup(bot: Bot, config: Config, sm):
    """Вызывает бэкап и отправляет его"""
    backup_paths = []

    users_path = await backup_users(sm)
    backup_paths.append(users_path)

    await send_backup_files(
        bot=bot, config=config, paths=backup_paths)

    for path in backup_paths:
        os.remove(path)
