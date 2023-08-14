from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from rest_framework import status, viewsets, mixins
from rest_framework.permissions import IsAuthenticated, BasePermission
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


class CreateOnlyModelViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    pass


class CreateListViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    pass


class IsUnauthenticated(BasePermission):
    def has_permission(self, request, view):
        return not (request.user and request.user.is_authenticated)


class MessageViewSet(CreateRetrieveListModelViewSet):
    serializer_class = serializers.MessageSerializer
    permission_classses = [IsAuthenticated]
    queryset = models.MessageModel.objects.all()

    def get_queryset(self):
        if not (self.request.user and self.request.user.is_authenticated):
            return self.queryset.none()
        else:
            return super().get_queryset().filter(author=self.request.user)


class RegisterUserView(CreateOnlyModelViewSet):
    serializer_class = serializers.RegisterUserSerializer
    permission_classes = [IsUnauthenticated]
    queryset = get_user_model().objects.all()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        return HttpResponseRedirect(redirect_to="/api/auth/login/")


class TokenView(CreateListViewSet):
    serializer_class = serializers.TokenSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.TokenModel.objects.all()

    def get_queryset(self):
        if not (self.request.user and self.request.user.is_authenticated):
            return self.queryset.none()
        else:
            return super().get_queryset().filter(user=self.request.user)
