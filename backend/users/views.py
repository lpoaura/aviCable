# from django.shortcuts import render

# Create your views here.

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import CustomUserSerializer, UserRegistrationSerializer


class UserViewSet(ModelViewSet):
    """A simple viewset to retrieve all the news items"""

    serializer_class = CustomUserSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()

    # def get_queryset(self):
    # queryset = super().get_queryset()
    # if not self.request.auth:
    #     return queryset.filter(private=False)
    # return queryset

    def get_permission_classes(self):
        if self.request.method == "post":
            return []
        else:
            return [IsAuthenticated]

    def get_serializer_class(self):
        if not self.request.user and self.request.method == "post":
            return UserRegistrationSerializer
        return super().get_serializer_class()


def verify_email(request, token):
    json_resp = {}
    try:
        user = User.objects.get(registration_token=token)
        if not user.email_verified:
            user.email_verified = True
            user.save()
            json_resp = {
                "type": "success",
                "msg": _("Email succesfully verified"),
            }
        else:
            json_resp = {"type": "info", "msg": _("Email already verified")}
    except ObjectDoesNotExist:
        json_resp = {"type": "error", "msg": _("User does not exists")}
    return JsonResponse(json_resp)
