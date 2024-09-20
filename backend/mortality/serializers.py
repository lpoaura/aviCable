import logging

from geo_area.models import GeoArea
from geo_area.serializers import GeoAreaSerializer
from rest_framework.exceptions import APIException
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from sinp_nomenclatures.serializers import NomenclatureSerializer
from species.serializers import SpeciesSerializer

from .models import Mortality

logger = logging.getLogger(__name__)

class MortalitySerializer(GeoFeatureModelSerializer):
    """Serializer for Mortality

    Used to serialize all data from mortality cases.
    """

    # Allow to display nested data
    species = SpeciesSerializer(read_only=True)
    death_cause = NomenclatureSerializer(read_only=True)

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
            "nb_death",
            "author",
            "data_source",
            "data_source_url",
            "created_by",
            "media",
            "comment",
        ]
        # Allow to handle create/update/partial_update with nested data
        extra_kwargs = {
            "species_id": {"source": "species", "write_only": True},
            "death_cause_id": {"source": "death_cause", "write_only": True},
        }


class MortalityWithAreasSerializer(GeoFeatureModelSerializer):
    """Serializer for Mortality

    Used to serialize all data from mortality cases.
    """

    # Allow to display nested data
    species = SpeciesSerializer(read_only=True)
    death_cause = NomenclatureSerializer(read_only=True)
    areas = GeoAreaSerializer(many=True, read_only=True)
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
            "nb_death",
            "author",
            "data_source",
            "data_source_url",
            "created_by",
            "media",
            "comment",
            "areas",
        ]
        # Allow to handle create/update/partial_update with nested data
        extra_kwargs = {
            "species_id": {"source": "species", "write_only": True},
            "death_cause_id": {"source": "death_cause", "write_only": True},
        }


    def create(self, validated_data):
        # create Point object with given coordinates
        item = self.Meta.model.objects.create(**validated_data)

        try:
            # get lists of GeoArea and Sensitive_Area that intersect with Point location
            geoareas = GeoArea.objects.all().filter(
                geom__intersects=point.geom
            )
            # set the lists to point.geo_area and save it
            item.areas.set(geoareas)
            item.save()

        except Exception:
            if item is not None:
                item.delete()
            msg = "Issue with attachment from new point to sensitive/geo areas. No Point created."
            logger.error(msg)
            raise APIException(msg)

        return item