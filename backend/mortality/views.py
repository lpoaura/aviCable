from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated  # DjangoModelPermissions,
from rest_framework_gis.filters import InBBOXFilter

from .models import Mortality
from .serializers import MortalitySerializer


class MortalityViewSet(viewsets.ModelViewSet):
    """ViewSet for Mortality item"""

    serializer_class = MortalitySerializer
    filter_backends = [InBBOXFilter,]
    bbox_filter_field = 'geom'
    permission_classes = [IsAuthenticated,]
    queryset = (
        Mortality.objects.all()
        .select_related("species")
        .select_related("infrstr")
        .select_related("infrstr__owner")
        .select_related('death_cause__type')
        .select_related('data_source')
        .prefetch_related('media')
    )
