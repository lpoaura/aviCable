from django.urls import path

from .views import (  # ActionViewSet,
    DiagnosisViewSet,
    InfrastructureViewSet,
    LineViewSet,
    OperationViewSet,
    PointViewSet,
)

urlpatterns = [
    # No create, update or delete on Infrastructure parent class: to be done on inherited classes
    path(
        "infrastructures/",
        InfrastructureViewSet.as_view({"get": "list"}),
        name="infrastructure_list",
    ),
    path(
        "infrastructures/<int:pk>/",
        InfrastructureViewSet.as_view({"get": "retrieve"}),
        name="infrastructure_detail",
    ),
    path(
        "points/",
        PointViewSet.as_view({"get": "list", "post": "create"}),
        # PointViewSet.as_view({"get": "list"}),
        name="point_list",
    ),
    path(
        "points/<int:pk>/",
        PointViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="point_detail",
    ),
    path(
        "lines/",
        LineViewSet.as_view({"get": "list", "post": "create"}),
        name="line_list",
    ),
    path(
        "lines/<int:pk>/",
        LineViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="line_detail",
    ),
    # No create, update or delete on Infrastructure parent class: to be done on inherited classes
    # path(
    #     "actions/",
    #     ActionViewSet.as_view({"get": "list"}),
    #     name="action_list",
    # ),
    # path(
    #     "actions/<int:pk>/",
    #     ActionViewSet.as_view({"get": "retrieve"}),
    #     name="action_detail",
    # ),
    path(
        "diagnosis/",
        DiagnosisViewSet.as_view({"get": "list", "post": "create"}),
        name="diag_list",
    ),
    path(
        "diagnosis/<int:pk>/",
        DiagnosisViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="diag_detail",
    ),
    path(
        "operations/",
        OperationViewSet.as_view(
            {"get": "list", "post": "create", "put": "update"}
        ),
        name="operation_list",
    ),
    path(
        "operations/<int:pk>/",
        OperationViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="operation_detail",
    ),
]
