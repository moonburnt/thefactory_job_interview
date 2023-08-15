from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from uuid import uuid4
import logging

log = logging.getLogger(__name__)


class MessageModel(models.Model):
    author = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="messages",
    )

    message = models.TextField()
    created = models.DateTimeField(auto_now=True, editable=False)


class TokenModel(models.Model):
    user = models.OneToOneField(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="tg_bot_token",
    )

    token = models.UUIDField(unique=True, default=uuid4, editable=False)


from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=MessageModel)
def on_message_save(sender, instance, **kwargs):
    from bot.models import TgUserModel
    from requests import post

    bot_token = instance.author.tg_bot_token
    if bot_token:
        tg_user = TgUserModel.objects.filter(token=bot_token).first()
        if tg_user:
            try:
                post(
                    url=settings.BOT_SETTINGS["URL"],
                    json={
                        "chat_id": str(tg_user.user_id),
                        "message": "asda",
                    },
                )
            except Exception as e:
                log.warning(e)
