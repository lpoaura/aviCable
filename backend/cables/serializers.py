import logging

from rest_framework.exceptions import APIException
from rest_framework_gis.serializers import (
    GeoFeatureModelSerializer,
    GeometryField,
    ModelSerializer,
)
from rest_polymorphic.serializers import PolymorphicSerializer
from sinp_nomenclatures.serializers import (
    NomenclatureSerializer as NomenclatureSerializer,
)

from geo_area.models import GeoArea
from geo_area.serializers import GeoAreaSerializer
from media.serializers import MediaSerializer
from mortality.serializers import MortalitySimpleSerializer
from sensitive_area.models import SensitiveArea
from sensitive_area.serializers import SensitiveAreaSerializer
from users.serializers import UserSimpleSerializer

from .models import (
    Action,
    Diagnosis,
    Equipment,
    Infrastructure,
    Line,
    LineOperation,
    Operation,
    Point,
    PointOperation,
)

logger = logging.getLogger(__name__)


class ActionSerializer(ModelSerializer):
    """Serializer for Action

    Used to serialize all data from actions.
    """

    media = MediaSerializer(many=True)

    class Meta:
        model = Action
        fields = ["id", "infrastructure", "date", "remark", "media"]


class DiagnosisSerializer(ModelSerializer):
    """Serializer for Diagnosis

    Used to serialize all data from Diagnosis.
    """

    # Allow to display nested data
    arming = NomenclatureSerializer(many=True, read_only=True)
    pole_attractivity = NomenclatureSerializer(read_only=True)
    pole_dangerousness = NomenclatureSerializer(read_only=True)
    sgmt_moving_risk = NomenclatureSerializer(read_only=True)
    sgmt_topo_integr_risk = NomenclatureSerializer(read_only=True)
    sgmt_landscape_integr_risk = NomenclatureSerializer(read_only=True)
    media = MediaSerializer(many=True, read_only=True)
    created_by = UserSimpleSerializer(read_only=True)
    updated_by = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Diagnosis
        fields = [
            "id",
            "infrastructure",
            "date",
            "remark",
            "isolation_advice",
            "dissuasion_advice",
            "attraction_advice",
            "change_advice",
            "visibility_advice",
            "burial_advice",
            "technical_proposal",
            "arming",
            "arming_id",
            "pole_attractivity",
            "pole_attractivity_id",
            "pole_dangerousness",
            "pole_dangerousness_id",
            "sgmt_moving_risk",
            "sgmt_moving_risk_id",
            "sgmt_topo_integr_risk",
            "sgmt_topo_integr_risk_id",
            "sgmt_landscape_integr_risk",
            "sgmt_landscape_integr_risk_id",
            "media",
            "media_id",
            "last",
            "created_by",
            "updated_by",
            "timestamp_create",
            "timestamp_update",
        ]
        # Allow to handle create/update/partial_update with nested data
        extra_kwargs = {
            "arming_id": {"source": "arming", "write_only": True},
            "pole_attractivity_id": {
                "source": "pole_attractivity",
                "write_only": True,
            },
            "pole_dangerousness_id": {
                "source": "pole_dangerousness",
                "write_only": True,
            },
            "sgmt_moving_risk_id": {
                "source": "sgmt_moving_risk",
                "write_only": True,
            },
            "sgmt_topo_integr_risk_id": {
                "source": "sgmt_topo_integr_risk",
                "write_only": True,
            },
            "sgmt_landscape_integr_risk_id": {
                "source": "sgmt_landscape_integr_risk",
                "write_only": True,
            },
            "media_id": {"source": "media", "write_only": True},
        }

        """Overriden create method for Diagnosis

        This method was overidden to implement a customized behaviour specific to application structure.
        New Diagnosis related to an Infrastructure (Point or Line) is created with field "last=True". That means it is current state of diagnosis for the Infrastructure.
        In case of new Diagnosis on same Infrastructure, the new one is created with "last=True" as current one. Older ones (should be exactly 1) then become "last=False" due to this method.
        APIException is raised if there is not exactly 1 Diagnosis with "last=True". If issue occures, Diagnostic is deleted (if it was created), previous current Diagnosis is set to last=True and an APIException is raised.

        Arguments:
            validated_data {dict} -- contains data for new Diagnosis creation

        Raises:
            APIException -- In case of issue with create process. If process fails, any new object created will be deleted before raising new APIException

        Returns:
            {Diagnosis} -- returns new Diagnosis object
        """

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        validated_data["updated_by"] = user
        validated_data["last"] = True
        Diagnosis.objects.all().filter(
            infrastructure=validated_data["infrastructure"], last=True
        ).update(last=False)

        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context["request"].user
        validated_data["updated_by"] = user
        return super().update(instance, validated_data)


class EquipmentSerializer(ModelSerializer):
    type = NomenclatureSerializer(read_only=True)

    class Meta:
        model = Equipment
        fields = [
            "id",
            "type_id",
            "type",
            "count",
            "reference",
            "comment",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "type_id": {"source": "type", "write_only": True},
        }

    def __init__(self, *args, **kwargs):
        super(EquipmentSerializer, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields[
                "id"
            ].required = (
                False  # Make id field not required for existing instances
            )

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        validated_data["updated_by"] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Prevent updating the id field
        user = self.context["request"].user
        validated_data["updated_by"] = user
        validated_data.pop("id", None)
        return super().update(instance, validated_data)


class OperationSerializer(ModelSerializer):
    """Serializer for Operation

    Used to serialize all data from operations.
    """

    # Allow to display nested data
    equipments = EquipmentSerializer(many=True, read_only=True)
    media = MediaSerializer(many=True, read_only=True)
    created_by = UserSimpleSerializer(read_only=True)
    updated_by = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Operation
        # geo_field = "geom"
        fields = [
            "id",
            "infrastructure",
            "date",
            "neutralization_level",
            "remark",
            "equipments",
            "media",
            "media_id",
            "last",
            "created_by",
            "updated_by",
            "timestamp_create",
            "timestamp_update",
            # "geom",
        ]
        # Allow to handle create/update/partial_update with nested data
        extra_kwargs = {
            "media_id": {"source": "media", "write_only": True},
        }

        """Overriden create method for Operation

        This method was overidden to implement a customized behaviour specific to application structure.
        New Operation related to an Infrastructure (Point or Line) is created with field "last=True". That means it is current state of diagnosis for the Infrastructure.
        In case of new Diagnosis on same Infrastructure, the new one is created with "last=True" as current one. Older ones (should be exactly 1) then become "last=False" due to this method.
        APIException is raised if there is not exactly 1 Operation with "last=True". If issue occures, Operation is deleted (if it was created), previous current Operation is set to last=True and an APIException is raised.

        Arguments:
            validated_data {dict} -- contains data for new Operation creation

        Raises:
            APIException -- In case of issue with create process. If process fails, any new object created will be deleted before raising new APIException

        Returns:
            {Operation} -- returns new Operation object
        """


class BaseOperationSerializer(GeoFeatureModelSerializer):
    equipments = EquipmentSerializer(many=True)
    geom = GeometryField(required=False, allow_null=True)
    media = MediaSerializer(many=True, read_only=True)
    created_by = UserSimpleSerializer(read_only=True)
    updated_by = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Operation
        geo_field = None
        abstract = True
        fields = [
            "id",
            "infrastructure",
            "date",
            "neutralization_level",
            "remark",
            "equipments",
            "media",
            "media_id",
            "last",
            "geom",
            "created_by",
            "updated_by",
            "timestamp_create",
            "timestamp_update",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "media_id": {"source": "media", "write_only": True},
        }

    def update(self, instance, validated_data):
        logger.debug("<PointOperationSerializer.update>")
        user = self.context["request"].user
        validated_data["updated_by"] = user
        if "geom" not in validated_data or validated_data["geom"] is None:
            validated_data["geom"] = validated_data.infrastructure.geom

        logger.debug(
            f"<BaseOperationSerializer.update> validated_data {validated_data}"
        )

        equipments_list = validated_data.pop("equipments")
        media = validated_data.pop("media", [])

        equipments = []
        for equipment_data in equipments_list:
            equipment_id = equipment_data.pop("id", None)
            equipment, _created = Equipment.objects.update_or_create(
                id=equipment_id, defaults=equipment_data
            )
            equipments.append(equipment)

        instance.equipments.set(equipments)
        instance.media.set(media)
        return instance

    def create(self, validated_data):
        logger.debug("<BaseOperationSerializer.create>")
        user = self.context["request"].user
        validated_data["created_by"] = user
        validated_data["updated_by"] = user
        if "geom" not in validated_data or validated_data["geom"] is None:
            validated_data["geom"] = validated_data.get("infrastructure").geom

        logger.debug(
            f"<BaseOperationSerializer.create> validated_data {validated_data}"
        )

        equipments_list = validated_data.pop("equipments", [])
        media = validated_data.pop("media", [])

        # Create the PointOperation instance
        operation = self.Meta.model.objects.create(**validated_data)

        equipments = []
        for equipment_data in equipments_list:
            # Create the Equipment instance
            equipment = Equipment.objects.create(**equipment_data)
            equipments.append(equipment)

        # Optionally, you can set the equipments to the point_operation if needed
        operation.equipments.set(equipments)
        operation.media.set(media)
        Operation.objects.filter(
            infrastructure=validated_data["infrastructure"], last=True
        ).exclude(pk=operation.id).update(last=False)
        return operation


class PointOperationSerializer(BaseOperationSerializer):
    class Meta:
        model = PointOperation
        geo_field = "geom"
        fields = [
            "id",
            "infrastructure",
            "date",
            "neutralization_level",
            "remark",
            "equipments",
            "media",
            "media_id",
            "last",
            "geom",
            "created_by",
            "updated_by",
            "timestamp_create",
            "timestamp_update",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "media_id": {"source": "media", "write_only": True},
        }


class LineOperationSerializer(BaseOperationSerializer):
    class Meta:
        model = LineOperation
        geo_field = "geom"
        fields = [
            "id",
            "infrastructure",
            "date",
            "neutralization_level",
            "remark",
            "equipments",
            "media",
            "media_id",
            "last",
            "geom",
            "created_by",
            "updated_by",
            "timestamp_create",
            "timestamp_update",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "media_id": {"source": "media", "write_only": True},
        }


class OperationPolymorphicSerializer(
    PolymorphicSerializer, GeoFeatureModelSerializer
):
    """Serializer for Infrastructure taking into account polymorphism

    Used to serialize all data from infrastructures.
    This allow handle specific data for classe inheriting from InfrastructureModel (e.g. Point, Line), as each object from inheriting classes are instances of InfrastructureModel.
    Inherit from PolymorphicSerializer.
    """

    model_serializer_mapping = {
        Operation: OperationSerializer,
        PointOperation: PointOperationSerializer,
        LineOperation: LineOperationSerializer,
    }

    class Meta:
        model = Operation
        geo_field = "geom"
        fields = "__all__"


class InfrastructureSerializer(ModelSerializer):
    """Serializer for Infrastructure

    Used to serialize all data from infrastructures.
    inherit from GeoAreaSerializer as contains geo data.
    """

    # Allow to display nested data
    network_type = NomenclatureSerializer()
    areas = GeoAreaSerializer(many=True)
    sensitive_area = SensitiveAreaSerializer(many=True)
    diagnosis = DiagnosisSerializer(many=True)
    operations = OperationSerializer(many=True)
    mortality = MortalitySimpleSerializer(many=True)

    class Meta:
        model = Infrastructure
        fields = [
            "id",
            "network_type",
            "geom",
            "areas",
            "sensitive_area",
            "diagnosis",
            "operations",
            "mortality",
        ]


class ActionPolymorphicSerializer(PolymorphicSerializer):
    """Serializer for Action taking into account polymorphismrequest"""

    model_serializer_mapping = {
        Action: ActionSerializer,
        Diagnosis: DiagnosisSerializer,
        Operation: OperationSerializer,
    }


class InstrastructureAbstractSerializer(GeoFeatureModelSerializer):
    network_type = NomenclatureSerializer(read_only=True)
    areas = GeoAreaSerializer(many=True, read_only=True)
    sensitive_area = SensitiveAreaSerializer(many=True, read_only=True)
    diagnosis = DiagnosisSerializer(many=True, read_only=True)
    operations = OperationSerializer(many=True, read_only=True)
    mortality = MortalitySimpleSerializer(many=True, read_only=True)
    created_by = UserSimpleSerializer(read_only=True)
    updated_by = UserSimpleSerializer(read_only=True)

    class Meta:
        abstract = True

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        validated_data["updated_by"] = user
        infrst = self.Meta.model.objects.create(**validated_data)

        try:
            # get lists of GeoArea and Sensitive_Area that intersect with Line location
            geoareas = GeoArea.objects.all().filter(
                geom__intersects=infrst.geom
            )
            sensitiveareas = SensitiveArea.objects.all().filter(
                geom__intersects=infrst.geom
            )
            # set the lists to line.geo_area and save it
            infrst.areas.set(geoareas)
            infrst.sensitive_area.set(sensitiveareas)
            infrst.save()

        except Exception:
            if infrst is not None:
                infrst.delete()
            msg = "Issue with attachment from new Line to sensitive/geo areas. No Line created."
            logger.error(msg)
            raise APIException(msg)

        return infrst

    def update(self, instance, validated_data):
        user = self.context["request"].user
        validated_data["updated_by"] = user
        return super().update(instance, validated_data)


class PointSerializer(InstrastructureAbstractSerializer):
    """Serializer for Point

    Used to serialize all data from Point.
    inherit from GeoAreaSerializer as contains geo data.
    """

    class Meta:
        model = Point
        geo_field = "geom"
        fields = [
            "id",
            "geom",
            "network_type",
            "network_type_id",
            "areas",
            # "geo_area_id",
            "sensitive_area",
            # "sensitive_area_id",
            "diagnosis",
            "operations",
            "mortality",
            "created_by",
            "updated_by",
            "timestamp_create",
            "timestamp_update",
        ]
        # Allow to handle create/update/partial_update with nested data
        extra_kwargs = {
            "network_type_id": {"source": "network_type", "write_only": True},
            # "geo_area_id": {"source": "geo_area", "write_only": True},
            # "sensitive_area_id": {"source": "sensitive_area", "write_only": True},
        }

        """ Overidden method to create Point

        At Point creation, method search all GeoArea and all SensitiveArea that intersects with new Point coordinates, and set GeoArea id list to Point field geo_area (Infrastructure.geo_area) and SensitiveArea id list to Point field sensitive_area (Infrastructure.sensitive_area).
        If issue occures for attachment with sensitive/geo areas, the Point is deleted (if it was created) and an APIException is raised.

        Arguments:
            validated_data {dict} -- contains data for new Point creation

        Raises:
            APIException -- In case of issue with create process. If process fails, any new object created will be deleted before raising new APIException

        Returns:
            {Point} -- returns new Point object
        """


class LineSerializer(InstrastructureAbstractSerializer):
    """Serializer for Line

    Used to serialize all data from lines.
    inherit from GeoAreaSerializer as contains geo data.
    """

    class Meta:
        model = Line
        geo_field = "geom"
        fields = [
            "id",
            "geom",
            "network_type",
            "network_type_id",
            "areas",
            # "geo_area_id",
            "sensitive_area",
            # "sensitive_area_id",
            "diagnosis",
            "operations",
            "mortality",
            "created_by",
            "updated_by",
            "timestamp_create",
            "timestamp_update",
        ]
        # Allow to handle create/update/partial_updcreateate with nested data
        extra_kwargs = {
            "network_type_id": {"source": "network_type", "write_only": True},
            # "geo_area_id": {"source": "geo_area", "write_only": True},
            # "sensitive_area_id": {"source": "sensitive_area", "write_only": True},
        }

        """ Overidden method to create Line

        At Line creation, method search all GeoArea and all SensitiveArea that intersects with new Line coordinates, and set GeoArea id list to Point field geo_area (Infrastructure.geo_area) and SensitiveArea id list to Line field sensitive_area (Infrastructure.sensitive_area).
        If issue occures for attachment with sensitive/geo areas, the Line is deleted (if it was created) and an APIException is raised.

        Arguments:
            validated_data {dict} -- contains data for new Line creation

        Raises:
            APIException -- In case of issue with create process. If process fails, any new object created will be deleted before raising new APIException

        Returns:
            {Line} -- returns new Line object
        """


class InfrastructurePolymorphicSerializer(
    PolymorphicSerializer, GeoFeatureModelSerializer
):
    """Serializer for Infrastructure taking into account polymorphism

    Used to serialize all data from infrastructures.
    This allow handle specific data for classe inheriting from InfrastructureModel (e.g. Point, Line), as each object from inheriting classes are instances of InfrastructureModel.
    Inherit from PolymorphicSerializer.
    """

    model_serializer_mapping = {
        Infrastructure: InfrastructureSerializer,
        Point: PointSerializer,
        Line: LineSerializer,
    }

    class Meta:
        model = Infrastructure
        geo_field = "geom"
        fields = "__all__"
