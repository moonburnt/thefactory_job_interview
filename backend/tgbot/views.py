from django.shortcuts import render
from rest_framework import status, viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from . import serializers
from . import models


class CreateRetrieveListModelViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    pass

class MessageViewSet(CreateRetrieveListModelViewSet):
    serializer_class = serializers.MessageSerializer
    permission_classses = [IsAuthenticated]
    queryset = models.MessageModel.objects.all()
