from rest_framework import serializers
from .models import MessageModel
import logging

log = logging.getLogger(__name__)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageModel
        fields = "__all__"
        read_only_fields = ("author",)
