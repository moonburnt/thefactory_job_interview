from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import MessageModel, TokenModel
import logging

log = logging.getLogger(__name__)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageModel
        # fields = "__all__"
        exclude = ("author",)
        # read_only_fields = ("author",)

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["author"] = request.user
        else:
            raise serializers.ValidationError("Expected authenticated user")

        return validated_data


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "password",
        )
        extra_kwargs = {k: {"required": True} for k in fields}

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()

        return user


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenModel
        fields = ("token",)

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        else:
            raise serializers.ValidationError("Expected authenticated user")

        if self.Meta.model.objects.filter(user=user).count() > 0:
            raise serializers.ValidationError("User already has token")

        validated_data["user"] = user

        return validated_data
