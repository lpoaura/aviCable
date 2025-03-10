# from django.shortcuts import render

# Create your views here.

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import CustomUserSerializer


class UserViewSet(ModelViewSet):
    """A simple viewset to retrieve all the news items"""

    serializer_class = CustomUserSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.auth:
            return queryset.filter(private=False)
        return queryset

    def get_permission_classes(self):
        if self.request.method == "post":
            return []
        else:
            return [IsAuthenticated]
