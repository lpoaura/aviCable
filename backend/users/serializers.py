# from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from sinp_nomenclatures.serializers import NomenclatureSerializer
from sinp_organisms.models import OrganismMember
from sinp_organisms.serializers import OrganismSerializer

from .models import User

UserModel = get_user_model()


class OrganismMemberSetSerializer(ModelSerializer):
    organism = OrganismSerializer()
    member_level = NomenclatureSerializer(many=True)

    class Meta:
        model = OrganismMember
        fields = "__all__"


class UserRegistrationSerializer(ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            "username",
            "first_name",
            "last_name",
            "password",
            "email",
            "phone",
            # "organism",
            "areas",
        ]

        # def update(self, instance, validated_data):
        #     if 'password' in validated_data:
        #         password = validated_data.pop('password')
        #         instance.set_password(password)
        #     return super().update(instance, validated_data)

        extra_kwargs = {
            "password": {"write_only": True},
            "id": {"read_only": True},
        }


    def create(self, validated_data):
        """Custom create account"""
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        areas = validated_data.pop('areas')
        user = UserModel.objects.create_user(username=username, email=email, password=password, **validated_data)
        user.areas.set(areas)
        return user


    # def create(self, validated_data):
    #     user = UserModel(**validated_data)
    #     # Hash the user's password.
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user


    


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
            "full_name",
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
