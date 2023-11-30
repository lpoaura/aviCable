from rest_framework.serializers import ModelSerializer

from .models import BaseLayers


class BaseLayersSerializer(ModelSerializer):
    """Base layers serializer

    Used to serialize all data from mortality cases.
    """

    class Meta:
        model = BaseLayers
        fields = [
            "id",
            "name",
            "url",
            "attribution",
            "default",
            "layer_type",
        ]
