from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiohttp import web
from .models import TgUserModel
from api.models import TokenModel
import asyncio
from typing import Optional
from uuid import UUID
import logging

log = logging.getLogger(__name__)


async def on_startup(dispatcher: Dispatcher):
    bot_info = await dispatcher.bot.get_me()
    log.info(f"Running WeatherBot as @{bot_info.username} ({bot_info.first_name})")


async def on_shutdown(dispatcher: Dispatcher):
    log.info("Shutting down the bot")


class EchoBot(Bot):
    def __init__(self, token: str):
        super().__init__(token=token)
        self.dp = Dispatcher(self, storage=MemoryStorage())
        self.web_app = web.Application()

    def run(self, host, port):
        print("Running echo bot")
        asyncio.get_event_loop().create_task(
            web._run_app(
                app=self.web_app,
                host=host,
                port=port,
            )
        )

        executor.start_polling(
            self.dp,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
        )


def _configure_web_app(bot: EchoBot) -> EchoBot:
    routes = web.RouteTableDef()

    @routes.post("/")
    async def send_message(request):
        data = await request.json()
        try:
            await bot.send_message(
                data["chat_id"],
                data["message"],
            )
        except Exception as e:
            log.warning(e)

        return web.Response()

    bot.web_app.add_routes(routes)

    return bot


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

        resp = "Hello, I'm echo bot."

        if user_model.token:
            resp += " It seems like you are already connected to db with token"
        else:
            resp += " Send me your token to connect to db"

        await message.reply(resp)

    @bot.dp.message_handler()
    async def echo(message: types.Message):
        # Since bot always starts with /start command, no checks for empty there
        user_model = await TgUserModel.objects.filter(
            user_id=message.from_user.id
        ).afirst()

        current_token = await TokenModel.objects.filter(tg_user=user_model).afirst()
        if current_token:
            await message.reply(
                f"You've already attached token '{current_token.token}'"
            )

        else:
            try:
                token_uuid = UUID(message.text)
            except ValueError:
                await message.reply("Invalid token format")
            else:
                token_model = await TokenModel.objects.filter(
                    token=token_uuid,
                ).afirst()

                if not token_model:
                    await message.reply("No such token")

                if await TgUserModel.objects.filter(token=token_model).afirst():
                    await message.reply("Token already in use")

                user_model.token = token_model
                await user_model.asave(update_fields=("token",))

                await message.reply(f"Successfully attached token '{message.text}'")

    bot = _configure_web_app(bot)

    return bot
