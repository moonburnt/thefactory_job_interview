from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import MessageViewSet, RegisterUserView, TokenView
import logging

log = logging.getLogger(__name__)


router = DefaultRouter()
router.register("message", MessageViewSet)
router.register("auth/register", RegisterUserView)
router.register("token", TokenView)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("rest_framework.urls")),
]
