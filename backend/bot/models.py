from django.db import models
import logging

log = logging.getLogger(__name__)


class TgUserModel(models.Model):
    token = models.OneToOneField(
        to="api.TokenModel",
        on_delete=models.CASCADE,
        related_name="tg_user",
        null=True,
        default=None,
    )

    user_id = models.TextField(unique=True, editable=False)
