from django.db import models
from django.contrib.auth import get_user_model
import logging

log = logging.getLogger(__name__)


class MessageModel(models.Model):
    author = models.ForeignKey(
        to = get_user_model(),
        on_delete= models.CASCADE,
        related_name = "messages",
    )

    message = models.TextField()
    created = models.DateTimeField(auto_now=True, editable=False)
