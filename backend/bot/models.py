from django.db import models
from api.models import TokenModel
import logging

log = logging.getLogger(__name__)


class TgUserModel(models.Model):
    token = models.OneToOneField(
        to=TokenModel,
        on_delete=models.CASCADE,
        related_name="tg_bot_token",
        null=True,
        default=None,
    )

    user_id = models.TextField(unique=True, editable=False)


# TODO: add signal
# When message model gets created - if it has reference to user that has reference
# to token that has reference to tg user - bot sends message

# TODO: make bot a singletone
