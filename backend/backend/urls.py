from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tgbot.views import MessageViewSet, RegisterUserView
import logging

log = logging.getLogger(__name__)


router = DefaultRouter()
router.register("message", MessageViewSet)
router.register("auth/register", RegisterUserView)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("rest_framework.urls")),
]
