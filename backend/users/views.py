# from django.shortcuts import render

# Create your views here.

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet

from .models import User
from .serializers import (
    ActivateAccountSerializer,
    CustomUserSerializer,
    UserRegistrationSerializer,
)


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


# def verify_email(request, token):
#     json_resp = {}
#     try:
#         user = User.objects.get(registration_token=token)
#         if not user.email_verified:
#             user.email_verified = True
#             user.save()
#             json_resp = {
#                 "type": "success",
#                 "msg": _("Email succesfully verified"),
#             }
#         else:
#             json_resp = {"type": "info", "msg": _("Email already verified")}
#     except ObjectDoesNotExist:
#         json_resp = {"type": "error", "msg": _("User does not exists")}
#     return JsonResponse(json_resp)


class VerifyEmailView(APIView):
    def get(self, request, token):
        json_resp = {}
        try:
            user = User.objects.get(registration_token=token)
            if not user.email_verified:
                user.email_verified = True
                user.save()
                json_resp = {
                    "type": "success",
                    "msg": _("Email successfully verified"),
                }
            else:
                json_resp = {
                    "type": "info",
                    "msg": _("Email already verified"),
                }
        except User.DoesNotExist:
            json_resp = {"type": "error", "msg": _("User does not exist")}
            return Response(json_resp, status=status.HTTP_404_NOT_FOUND)

        return Response(json_resp, status=status.HTTP_200_OK)


class ActivateAccountViewSet(ViewSet):
    permission_classes = [IsAdminUser]  # Require authentication
    queryset = User.objects.all()
    lookup_field = "token"

    def retrieve(self, request, token=None):
        try:
            user = User.objects.get(
                registration_token=token
            )  # Get user by token
            serializer = CustomUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {"type": "error", "msg": _("User does not exist.")},
                status=status.HTTP_404_NOT_FOUND,
            )

    def partial_update(self, request, token=None):
        try:
            user = User.objects.get(
                registration_token=token
            )  # Get user by token
            serializer = ActivateAccountSerializer(
                user, data=request.data, partial=True
            )

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "type": "success",
                        "msg": _("Account activated successfully."),
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            return Response(
                {"type": "error", "msg": _("User does not exist.")},
                status=status.HTTP_404_NOT_FOUND,
            )
