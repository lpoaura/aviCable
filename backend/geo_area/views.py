from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework_gis.filters import InBBoxFilter

from .models import GeoArea
from .serializers import GeoAreaGeoSerializer


class GeoAreaViewSet(viewsets.ReadOnlyModelViewSet):
    """A simple viewset to retrieve all the GeoArea items"""

    serializer_class = GeoAreaGeoSerializer
    permission_classes = [IsAuthenticated]
    queryset = (
        GeoArea.objects.prefetch_related("type__parents")
        .select_related("type__type")
        .all()
    )
    filterset_fields = [
        "type__code",
    ]
    bbox_filter_field = "geom"
    filter_backends = (InBBoxFilter,)
    bbox_filter_include_overlapping = True
