from django.db import models
from django.contrib.auth import get_user_model
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
