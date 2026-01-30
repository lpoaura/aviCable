from rest_framework import viewsets
from rest_framework.permissions import (  # DjangoModelPermissions,
    IsAuthenticated,
)
from rest_framework_gis.filters import InBBOXFilter
from rest_framework.permissions import DjangoModelPermissions

from .models import Mortality
from .serializers import MortalitySerializer, MortalityWithAreasSerializer


class MortalityViewSet(viewsets.ModelViewSet):
    """ViewSet for Mortality item"""

    serializer_class = MortalitySerializer
    filter_backends = [
        InBBOXFilter,
    ]
    bbox_filter_field = "geom"
    permission_classes = [DjangoModelPermissions]
    queryset = (
        Mortality.objects.all()
        .select_related("species")
        .select_related("infrstr")
        .select_related("infrstr__network_type")
        .prefetch_related("infrstr__network_type__parents")
        .select_related("death_cause__type")
        .prefetch_related("death_cause__parents")
        .select_related("data_source")
        .select_related("created_by")
        .select_related("updated_by")
        .prefetch_related("media")
    )

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == "retrieve":
            return qs.prefetch_related("areas").prefetch_related("areas__type")
        return qs

    def get_serializer_class(self):
        if self.action == "retrieve":
            return MortalityWithAreasSerializer
        return super().get_serializer_class()
