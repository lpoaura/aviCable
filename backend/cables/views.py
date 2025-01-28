import logging

from django.db.models import Prefetch
from geo_area.models import GeoArea
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from rest_framework_gis.filters import InBBoxFilter

from .filters import InfrstrInBboxFilter
from .models import Diagnosis, Infrastructure, Line, Operation, Point
from .serializers import (DiagnosisSerializer,
                          InfrastructurePolymorphicSerializer, LineSerializer,
                          OperationPolymorphicSerializer, PointSerializer)

logger = logging.getLogger(__name__)


class InfrastructureViewSet(viewsets.ModelViewSet):
    """ViewSet for Infrastructure item"""

    serializer_class = InfrastructurePolymorphicSerializer
    # permission_classes = [DjangoModelPermissions]
    # Define queryset by optimizing DB requests
    filter_backends = (InfrstrInBboxFilter,)
    # bbox_filter_field = 'point__geom'
    bbox_filter_fields = ["point__geom", "line__geom"]
    bbox_filter_include_overlapping = True
    queryset = (
        Infrastructure.objects.all()
        .select_related("owner")
        .prefetch_related(
            Prefetch(
                "areas",
                queryset=GeoArea.objects.only("id", "code", "name", "type"),
            )
        )
        .prefetch_related("areas__type")
        .prefetch_related("sensitive_area")
        .prefetch_related("diagnosis")
        .prefetch_related("diagnosis__media")
        .prefetch_related("diagnosis__pole_type")
        .prefetch_related("diagnosis__pole_attractivity")
        .prefetch_related("diagnosis__pole_dangerousness")
        .prefetch_related("diagnosis__sgmt_moving_risk")
        .prefetch_related("diagnosis__sgmt_topo_integr_risk")
        .prefetch_related("diagnosis__sgmt_landscape_integr_risk")
        .prefetch_related("operations")
        .prefetch_related("operations__equipments")
        .prefetch_related("operations__equipments__type")
        .prefetch_related("operations__media")
        .prefetch_related("mortality")
    )

    # def get_bbox_filter_field(self):
    #     print(f'get_bbox_filter_field {dir(self)}')
    #     return 'point__geom'


class PointViewSet(viewsets.ModelViewSet):
    """ViewSet for Point item"""

    serializer_class = PointSerializer
    # permission_classes = [DjangoModelPermissions]
    filter_backends = (InBBoxFilter,)
    bbox_filter_field = "geom"
    bbox_filter_include_overlapping = True
    # Define queryset by optimizing DB requests
    queryset = (
        Point.objects.all()
        .select_related("owner")
        .prefetch_related("areas")
        .prefetch_related("sensitive_area")
    )


class LineViewSet(viewsets.ModelViewSet):
    """ViewSet for Line item"""

    serializer_class = LineSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = (InBBoxFilter,)
    bbox_filter_field = "geom"
    bbox_filter_include_overlapping = True
    # Define queryset by optimizing DB requests
    queryset = (
        Line.objects.all()
        .select_related("owner")
        .prefetch_related("areas")
        .prefetch_related("sensitive_area")
    )


# class ActionViewSet(viewsets.ModelViewSet):
#     """ViewSet for Action item"""

#     serializer_class = ActionPolymorphicSerializer
#     permission_classes = [DjangoModelPermissions]
#     queryset = Action.objects.all()


class DiagnosisViewSet(viewsets.ModelViewSet):
    """ViewSet for Diagnosis item"""

    serializer_class = DiagnosisSerializer
    permission_classes = [DjangoModelPermissions]
    queryset = Diagnosis.objects.all()

class OperationViewSet(viewsets.ModelViewSet):
    """ViewSet for Operation item"""

    serializer_class = OperationPolymorphicSerializer
    # permission_classes = [DjangoModelPermissions]
    queryset = (
        Operation.objects.all()
        .select_related("infrastructure")
        .prefetch_related("equipments")
        .prefetch_related("media")
        .prefetch_related("equipments__type")
    )
    # filterset_class = OperationFilter
    bbox_filter_fields = ["pointoperation__geom", "lineoperation__geom"]
    filter_backends = (InfrstrInBboxFilter,)
    bbox_filter_include_overlapping = True
