import asyncio
import argparse

from src.domain.base.exceptions.base import AppException
from src.tgbot.run import run_bot_polling, run_bot_webhook

parser = argparse.ArgumentParser(description='Videos to images')
parser.add_argument('--polling', action='store_true', help='Start bot on polling')
parser.add_argument('--webhook', action='store_true', help='Start bot on webhook')


if __name__ == "__main__":
    args = parser.parse_args()

    if args.polling and args.webhook:
        raise AppException('Please specify correct argument')

    if args.polling:
        asyncio.run(run_bot_polling())
    elif args.webhook:
        run_bot_webhook()
    else:
        asyncio.run(run_bot_polling())
