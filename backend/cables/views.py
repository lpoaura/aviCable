import logging

from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from rest_framework_gis.filters import InBBoxFilter

from .filters import OperationFilter
from .models import Action, Diagnosis, Infrastructure, Line, Operation, Point
from .serializers import (
    ActionPolymorphicSerializer,
    DiagnosisSerializer,
    InfrastructurePolymorphicSerializer,
    LineSerializer,
    OperationSerializer,
    PointSerializer,
)

logger = logging.getLogger(__name__)


class InfrastructureViewSet(viewsets.ModelViewSet):
    """ViewSet for Infrastructure item"""

    serializer_class = InfrastructurePolymorphicSerializer
    # permission_classes = [DjangoModelPermissions]
    # Define queryset by optimizing DB requests
    filter_backends = (InBBoxFilter,)
    bbox_filter_field = 'point__geom'
    queryset = (
        Infrastructure.objects.all()
        .select_related("owner")
        .prefetch_related("geo_area")
        .prefetch_related("geo_area__type")
        .prefetch_related("sensitive_area")
        .prefetch_related("actions_infrastructure")
        .prefetch_related('actions_infrastructure__media')
        .prefetch_related('actions_infrastructure__condition')
        .prefetch_related('actions_infrastructure__pole_type')
        .prefetch_related('actions_infrastructure__pole_attractivity')
        .prefetch_related('actions_infrastructure__pole_dangerousness')
        .prefetch_related('actions_infrastructure__sgmt_build_integr_risk')
        .prefetch_related('actions_infrastructure__sgmt_moving_risk')
        .prefetch_related('actions_infrastructure__sgmt_topo_integr_risk')
        .prefetch_related('actions_infrastructure__sgmt_veget_integr_risk')
    )


class PointViewSet(viewsets.ModelViewSet):
    """ViewSet for Point item"""

    serializer_class = PointSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = (InBBoxFilter,)
    # Define queryset by optimizing DB requests
    queryset = (
        Point.objects.all()
        .select_related("owner")
        .prefetch_related("geo_area")
        .prefetch_related("sensitive_area")
    )


class LineViewSet(viewsets.ModelViewSet):
    """ViewSet for Line item"""

    serializer_class = LineSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = (InBBoxFilter,)
    # Define queryset by optimizing DB requests
    queryset = (
        Line.objects.all()
        .select_related("owner")
        .prefetch_related("geo_area")
        .prefetch_related("sensitive_area")
    )


class ActionViewSet(viewsets.ModelViewSet):
    """ViewSet for Action item"""

    serializer_class = ActionPolymorphicSerializer
    permission_classes = [DjangoModelPermissions]
    queryset = Action.objects.all()


class DiagnosisViewSet(viewsets.ModelViewSet):
    """ViewSet for Diagnosis item"""

    serializer_class = DiagnosisSerializer
    permission_classes = [DjangoModelPermissions]
    queryset = Diagnosis.objects.all()


class OperationViewSet(viewsets.ModelViewSet):
    """ViewSet for Operation item"""

    serializer_class = OperationSerializer
    permission_classes = [DjangoModelPermissions]
    queryset = Operation.objects.all()
    filterset_class = OperationFilter
