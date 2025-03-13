# from django.core.mail import send_mail
from rest_framework.serializers import ModelSerializer
from sinp_nomenclatures.serializers import NomenclatureSerializer
from sinp_organisms.models import OrganismMember
from sinp_organisms.serializers import OrganismSerializer

from .models import User


class OrganismMemberSetSerializer(ModelSerializer):
    organism = OrganismSerializer()
    member_level = NomenclatureSerializer(many=True)

    class Meta:
        model = OrganismMember
        fields = "__all__"


class UserRegistrationSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "organism",
            "areas",
        ]

    # def create(self, validated_data):
    #     validated_data["active"] = False
    #     return super().create(validated_data)

    # def update(self, instance, validated_data):
    #     return super().update(instance, validated_data)


class UserSimpleSerializer(ModelSerializer):
    """Serializer for Media model"""

    class Meta:
        model = User
        fields = [
            "username",
            "full_name",
            "avatar",
        ]


class CustomUserSerializer(ModelSerializer):
    """Serializer for Media model"""

    organismmember_set = OrganismMemberSetSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "avatar",
            "organisms",
            "organismmember_set",
            "areas",
        ]

    # def create(self, validated_data):
    #     # user = self.context["request"].user
    #     # validated_data["created_by"] = user
    #     # validated_data["updated_by"] = user
    #     validated_data["is_active"] = False
    #     return super().create(validated_data)


class ActivateAccountSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["is_active"]
