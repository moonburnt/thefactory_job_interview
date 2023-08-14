from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from .models import TgUserModel
from typing import Optional

import logging

log = logging.getLogger(__name__)


async def on_startup(dispatcher: Dispatcher):
    bot_info = await dispatcher.bot.get_me()
    log.info(f"Running WeatherBot as @{bot_info.username} ({bot_info.first_name})")


async def on_shutdown(dispatcher: Dispatcher):
    log.info("Shutting down the bot")


class EchoBot(Bot):
    def __init__(self, token):
        super().__init__(token=token)
        self.dp = Dispatcher(self, storage=MemoryStorage())

    def run(self):
        executor.start_polling(
            self.dp,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
        )


def make_bot(token: str) -> EchoBot:
    bot = EchoBot(
        token=token,
    )

    @bot.dp.message_handler(commands=["start"])
    async def send_welcome(message: types.Message):
        """Handler used as response to /start command"""

        user_model = await TgUserModel.objects.filter(
            user_id=message.from_user.id
        ).afirst()
        if not user_model:
            user_model = await TgUserModel.objects.acreate(user_id=message.from_user.id)

        print(user_model)

        resp = "Hello, I'm echo bot."

        if user_model.token:
            resp += " It seems like you are already connected to db with token"
        else:
            resp += " Send me your token to connect to db"

        await message.reply(resp)

    return bot


# @dp.message_handler()
# async def echo(message: types.Message):
#     message.from_user.id
#     await message.answer(message.text)
