from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ActivateAccountViewSet, UserViewSet, VerifyEmailView

app_name = "users"

router = DefaultRouter()
router.register(r"", UserViewSet)
router.register(r"activate", ActivateAccountViewSet, "activate_user")

urlpatterns = [
    path(
        "verify_email/<str:token>/",
        VerifyEmailView.as_view(),
        name="verify_email",
    ),
    path("", include(router.urls)),
]
