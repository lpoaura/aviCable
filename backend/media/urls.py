from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MediaViewSet

app_name = "media"

router = DefaultRouter()
router.register(r'', MediaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path(
    #     "",
    #     MediaViewSet.as_view({"get": "list", "post": "create"}),
    #     name="media_list",
    # ),
    # path(
    #     "<int:pk>/",
    #     MediaViewSet.as_view(
    #         {
    #             "get": "retrieve",
    #             "patch": "update",
    #             "put": "partial_update",
    #             "delete": "destroy",
    #         }
    #     ),
    #     name="media_detail",
    # ),
]
