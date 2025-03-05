from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from .models import Species
from .serializers import SpeciesSerializer

# from rest_framework.permissions import (
#     IsAuthenticated,  # DjangoModelPermissions,
# )


class SpeciesViewSet(viewsets.ModelViewSet):
    """ViewSet for Species items"""

    serializer_class = SpeciesSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [
        SearchFilter,
    ]
    search_fields = [
        "=code",
        "scientific_name",
        "vernacular_name",
        "@scientific_name",
        "@vernacular_name",
    ]
    queryset = Species.objects.all()
