from rest_framework import viewsets

from .models import Mortality
from .serializers import MortalitySerializer

# from rest_framework.permissions import (
#     IsAuthenticated,  # DjangoModelPermissions,
# )


class MortalityViewSet(viewsets.ModelViewSet):
    """ViewSet for Mortality item"""

    serializer_class = MortalitySerializer
    # permission_classes = [IsAuthenticated]
    queryset = (
        Mortality.objects.all()
        .select_related("species")
        .select_related("infrstr")
        .select_related("infrstr__owner")
        .select_related('death_cause__type')
        .select_related('data_source')
        .prefetch_related('media')
    )
