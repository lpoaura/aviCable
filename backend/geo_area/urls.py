from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import GeoAreaViewSet

app_name = "geo_area"


router = DefaultRouter()
router.register(r"", GeoAreaViewSet, basename="geoarea")

urlpatterns = router.urls
