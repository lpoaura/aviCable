from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions

from .models import Media
from .serializers import MediaSerializer


class MediaViewSet(viewsets.ModelViewSet):
    """A simple viewset to retrieve all the Media items"""

    serializer_class = MediaSerializer
    # permission_classes = [DjangoModelPermissions]
    queryset = Media.objects.all()
