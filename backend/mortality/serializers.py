import logging

from rest_framework.serializers import ModelSerializer
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from sinp_nomenclatures.serializers import NomenclatureSerializer

from cables.models import Infrastructure
from geo_area.models import GeoArea
from geo_area.serializers import GeoAreaSerializer
from media.serializers import MediaSerializer
from species.serializers import SpeciesSerializer
from users.serializers import UserSimpleSerializer

from .models import Mortality

logger = logging.getLogger(__name__)


class MortalityInfrastructureSerializer(ModelSerializer):
    owner = NomenclatureSerializer(read_only=True)

    class Meta:
        model = Infrastructure
        fields = [
            "id",
            "owner",
        ]


class MortalitySimpleSerializer(ModelSerializer):
    """Serializer for Mortality

    Used to serialize all data from mortality cases.
    """

    # Allow to display nested data
    species = SpeciesSerializer(read_only=True)
    death_cause = NomenclatureSerializer(read_only=True)
    created_by = UserSimpleSerializer(read_only=True)
    updated_by = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Mortality
        fields = [
            "id",
            "geom",
            "date",
            "species",
            "death_cause",
            "infrstr",
            "nb_death",
            "author",
            "data_source",
            "data_source_url",
            "media",
            "comment",
            "created_by",
            "updated_by",
            "timestamp_create",
            "timestamp_update",
        ]


class MortalitySerializer(GeoFeatureModelSerializer):
    """Serializer for Mortality

    Used to serialize all data from mortality cases.
    """

    # Allow to display nested data
    species = SpeciesSerializer(read_only=True)
    death_cause = NomenclatureSerializer(read_only=True)
    infrstr = MortalityInfrastructureSerializer(read_only=True)
    created_by = UserSimpleSerializer(read_only=True)
    updated_by = UserSimpleSerializer(read_only=True)
    media = MediaSerializer(many=True, read_only=True)

    class Meta:
        model = Mortality
        geo_field = "geom"
        fields = [
            "id",
            "geom",
            "date",
            "species",
            "species_id",
            "death_cause",
            "death_cause_id",
            "infrstr",
            "infrstr_id",
            "nb_death",
            "author",
            "data_source",
            "data_source_url",
            "media",
            "media_id",
            "comment",
            "created_by",
            "updated_by",
            "timestamp_create",
            "timestamp_update",
        ]
        # Allow to handle create/update/partial_update with nested data
        extra_kwargs = {
            "species_id": {"source": "species", "write_only": True},
            "death_cause_id": {"source": "death_cause", "write_only": True},
            "infrstr_id": {"source": "infrstr", "write_only": True},
            "media_id": {"source": "media", "write_only": True},
            # "areas_id": {"source": "areas", "write_only": True},
        }

    def create(self, validated_data):
        # create Point object with given coordinates
        user = self.context["request"].user
        validated_data["created_by"] = user
        validated_data["updated_by"] = user
        validated_data["areas"] = GeoArea.objects.all().filter(
            geom__intersects=validated_data["geom"]
        )
        print(f"validated_data {validated_data}")

        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context["request"].user
        validated_data["updated_by"] = user
        validated_data["areas"] = GeoArea.objects.all().filter(
            geom__intersects=validated_data["geom"]
        )

        return super().update(instance, validated_data)


class MortalityWithAreasSerializer(MortalitySerializer):
    """Serializer for Mortality

    Used to serialize all data from mortality cases.
    """

    # Allow to display nested data
    areas = GeoAreaSerializer(many=True, read_only=True)

    class Meta:
        model = Mortality
        geo_field = "geom"
        fields = [
            "id",
            "geom",
            "date",
            "species",
            "death_cause",
            "infrstr",
            "nb_death",
            "author",
            "data_source",
            "data_source_url",
            "media",
            "comment",
            "areas",
            "created_by",
            "updated_by",
            "timestamp_create",
            "timestamp_update",
        ]
