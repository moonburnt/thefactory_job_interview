from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tgbot.views import MessageViewSet
import logging

log = logging.getLogger(__name__)

router = DefaultRouter()
router.register("message", MessageViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/auth/", include("rest_framework.urls")),
]
