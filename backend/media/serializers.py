from rest_framework.serializers import ModelSerializer

from .models import Media


class MediaSerializer(ModelSerializer):
    """Serializer for Media model"""

    class Meta:
        model = Media
        fields = [
            "id",
            "label",
            "storage",
            "date",
            "author",
            "source",
            "remark",
        ]

    # TODO: Set those functions after frontend will permit auth for formData posts
    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     validated_data['created_by'] = user
    #     validated_data['updated_by'] = user
    #     return super().create(validated_data)

    # def update(self, instance, validated_data):
    #     user = self.context['request'].user
    #     validated_data['updated_by'] = user
    #     return super().update(instance, validated_data)
