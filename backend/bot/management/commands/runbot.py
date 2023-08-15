from django.core.management.base import BaseCommand, CommandParser
from django.conf import settings
from bot.services import make_bot
from os import environ
from sys import exit
import logging

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Run telegram bot"

    def handle(self, *args, **options):
        settings.IS_BOT_INSTANCE = True

        token_name = "TG_TOKEN"
        token = environ.get(token_name)
        if token is None:
            log.critical(
                "Unable to find bot token. "
                f"Please, set '{token_name}' environment variable and try again"
            )
            exit(2)

        bot = make_bot(
            token=token,
        )
        bot.run(
            host=settings.BOT_SETTINGS["HOST"],
            port=settings.BOT_SETTINGS["PORT"],
        )
