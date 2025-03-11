from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, verify_email

app_name = "users"

router = DefaultRouter()
router.register(r"", UserViewSet)

urlpatterns = [
    path("verify_email/<str:token>/", verify_email, name="verify_email"),
    path("", include(router.urls)),
]
