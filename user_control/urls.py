from django.urls import path, include
from .views import (
    CreateUserView, LoginView, UpdatePasswordView,
    MeView
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

router.register("create-user", CreateUserView, 'create_user')
router.register("login", LoginView, 'login')
router.register("updated-password", UpdatePasswordView, 'updated_password')
router.register("me", MeView, 'me')

urlpatterns = [
    path("", include(router.urls))
]
