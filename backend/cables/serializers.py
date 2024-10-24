import logging

from geo_area.models import GeoArea
from geo_area.serializers import GeoAreaSerializer
from media.serializers import MediaSerializer
from mortality.serializers import MortalitySimpleSerializer
from rest_framework.exceptions import APIException
from rest_framework_gis.serializers import (GeoFeatureModelSerializer,
                                            GeometryField, ModelSerializer)
from rest_polymorphic.serializers import PolymorphicSerializer
from sensitive_area.models import SensitiveArea
from sensitive_area.serializers import SensitiveAreaSerializer
from sinp_nomenclatures.serializers import \
    NomenclatureSerializer as NomenclatureSerializer

from .models import (Action, Diagnosis, Equipment, Infrastructure, Line,
                     LineOperation, Operation, Point, PointOperation)

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
    pole_type = NomenclatureSerializer(many=True, read_only=True)
    pole_attractivity = NomenclatureSerializer(read_only=True)
    pole_dangerousness = NomenclatureSerializer(read_only=True)
    sgmt_moving_risk = NomenclatureSerializer(read_only=True)
    sgmt_topo_integr_risk = NomenclatureSerializer(read_only=True)
    sgmt_landscape_integr_risk = NomenclatureSerializer(read_only=True)
    media = MediaSerializer(many=True, read_only=True)

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
            "technical_proposal",
            "pole_type",
            "pole_type_id",
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
        ]
        # Allow to handle create/update/partial_update with nested data
        extra_kwargs = {
            "pole_type_id": {"source": "pole_type", "write_only": True},
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
        try:
            # define variables to be used in error handling if needed
            newDiag = None
            previous_current = []
            # get current Diagnosis before creation of new one (should be only one, but keep search for several. In case of several ones, this method will correct issue by setting all previous with last=False)
            old_diags = Diagnosis.objects.all().filter(
                infrastructure=validated_data["infrastructure"], last=True
            )
            for diag in old_diags:
                previous_current.append(
                    diag.id
                )  # keep id of current Diag before new one

            # gather data for ManyToMany fields (and removing related data from validated_data)
            poleType_data = None
            media_data = None
            if "pole_type" in validated_data:
                poleType_data = validated_data.pop("pole_type")
            if "media" in validated_data:
                media_data = validated_data.pop("media")

            # create new Diagnosis
            newDiag = Diagnosis.objects.create(**validated_data)
            if newDiag is not None:
                # set old current Diagnosis to last=False
                for diag in old_diags:
                    if diag.id != newDiag.id:
                        diag.last = False
                        diag.save()

                # set data to ManyToMany fields old newDiag
                if poleType_data is not None:
                    newDiag.pole_type.set(poleType_data)
                if media_data is not None:
                    newDiag.media.set(media_data)

        # Error handling: newDiag is deleted if exists, and previous current Diag come back with
        # last=True. Django would send Response with status code 500 and defined message
        except Exception:
            if newDiag is not None:
                newDiag.delete()
                for id in previous_current:
                    Diagnosis.objects.get(id=id).update(last=True)

            msg = "Issue with Diagnosis configuration. No Diagnosis created."
            logger.error(msg)
            raise APIException(msg)

        return newDiag  # returns new Diag if success


class EquipmentSerializer(ModelSerializer):
    type = NomenclatureSerializer(read_only=True)

    class Meta:
        model = Equipment
        fields = ["id", "type_id", "type", "count", "reference", "comment"]
        extra_kwargs = {
            "id": {"read_only": True},
            "type_id": {"source": "type", "write_only": True},
        }

    def __init__(self, *args, **kwargs):
        super(EquipmentSerializer, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields["id"].required = (
                False  # Make id field not required for existing instances
            )

    def update(self, instance, validated_data):
        # Prevent updating the id field
        validated_data.pop("id", None)
        return super().update(instance, validated_data)


class OperationSerializer(ModelSerializer):
    """Serializer for Operation

    Used to serialize all data from operations.
    """

    # Allow to display nested data
    equipments = EquipmentSerializer(many=True, read_only=True)
    media = MediaSerializer(many=True, read_only=True)

    class Meta:
        model = Operation
        # geo_field = "geom"
        fields = [
            "id",
            "infrastructure",
            "date",
            "remark",
            "equipments",
            "media",
            "media_id",
            "last",
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

    def create(self, validated_data):
        try:
            # define variables to be used in error handling if needed
            newOp = None
            previous_current = []
            # get current Operation before creation of new one (should be only one, but keep
            # search for several. In case of several ones, this method will correct issue by
            # setting all previous with last=False)
            old_ops = Operation.objects.all().filter(
                infrastructure=validated_data["infrastructure"], last=True
            )
            for op in old_ops:
                previous_current.append(
                    op.id
                )  # keep id of current Operation before new one

            # gather data for ManyToMany fields (and removing related data from validated_data)
            eqmtType_data = None
            media_data = None
            if "eqmt_type" in validated_data:
                eqmtType_data = validated_data.pop("eqmt_type")
            if "media" in validated_data:
                media_data = validated_data.pop("media")

            # create new Operation
            newOp = Operation.objects.create(**validated_data)

            if newOp is not None:
                # set old current Diagnosis to last=False
                for op in old_ops:
                    if op.id != newOp.id:
                        op.last = False
                        op.save()
                # set data to ManyToMany fields old newDiag
                if eqmtType_data is not None:
                    newOp.eqmt_type.set(eqmtType_data)
                if media_data is not None:
                    newOp.media.set(media_data)

        # Error handling: newOp is deleted if exists, and previous current Operation come back with
        # last=True. Django would send Response with status code 500 and defined message
        except Exception:
            if newOp is not None:
                newOp.delete()
                for id in previous_current:
                    Operation.objects.get(id=id).update(last=True)

            msg = "Issue with Diagnosis configuration. No Diagnosis created."
            logger.error(msg)
            raise APIException(msg)

        return newOp  # returns new Diag if success

class BaseOperationSerializer(GeoFeatureModelSerializer):
    equipments = EquipmentSerializer(many=True)
    media = MediaSerializer(many=True, read_only=True)

    class Meta:
        geo_field = "geom"
        fields = [
            "id",
            "infrastructure",
            "date",
            "remark",
            "equipments",
            "media",
            # "media_id",
            "last",
            "geom",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
        }

    def update(self, instance, validated_data):
        equipments_data = validated_data.pop("equipments")
        print('validated_data', validated_data)
        # equipments = instance.equipments.all()
        equipments = []
        for equipment_data in equipments_data:
            print(
                f"equipment_data.keys() {equipment_data.keys()} {equipment_data.get('id')}"
            )
            equipment_id = (
                equipment_data.get("id") if id in equipment_data else None
            )
            equipment_type_id = equipment_data.get("type")

            update_values = {
                "type": equipment_type_id,  # Assuming type is a foreign key to Nomenclature
                "count": equipment_data.get("count"),
                "reference": equipment_data.get("reference"),
                "comment": equipment_data.get("comment"),
            }

            equipment, _created = Equipment.objects.update_or_create(
                id=equipment_id, defaults=update_values
            )
            equipments.append(equipment)
        instance.equipments.set(equipments)
        # instance.equipments.
        return super().update(instance, validated_data)

    def create(self, validated_data):
        equipments_data = validated_data.pop("equipments", [])

        # Create the PointOperation instance
        point_operation = self.Meta.model.objects.create(**validated_data)

        equipments = []
        for equipment_data in equipments_data:
            equipment_type_id = equipment_data.get("type")
            create_values = {
                "type": equipment_type_id,  # Assuming type is a foreign key to Nomenclature
                "count": equipment_data.get("count"),
                "reference": equipment_data.get("reference"),
                "comment": equipment_data.get("comment"),
            }

            # Create the Equipment instance
            equipment = Equipment.objects.create(**create_values)
            equipments.append(equipment)

        # Optionally, you can set the equipments to the point_operation if needed
        point_operation.equipments.set(equipments)
        Operation.objects.filter(
            infrastructure=validated_data["infrastructure"], last=True
        ).exclude(pk=point_operation.id).update(last=False)

        return point_operation



class PointOperationSerializer(GeoFeatureModelSerializer):
    equipments = EquipmentSerializer(many=True)
    geom = GeometryField(required=False, allow_null=True)

    class Meta:
        model = PointOperation
        geo_field = "geom"
        fields = [
            "id",
            "infrastructure",
            "date",
            "remark",
            "equipments",
            "media",
            # "media_id",
            "last",
            "geom",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
        }

    def update(self, instance, validated_data):
        equipments_data = validated_data.pop("equipments")
        if 'geom' not in validated_data or validated_data['geom'] is None:
            validated_data['geom'] = validated_data.infrastructure.geom
        # equipments = instance.equipments.all()
        equipments = []
        for equipment_data in equipments_data:
            print(
                f"equipment_data.keys() {equipment_data.keys()} {equipment_data.get('id')}"
            )
            equipment_id = (
                equipment_data.get("id") if id in equipment_data else None
            )
            equipment_type_id = equipment_data.get("type")

            update_values = {
                "type": equipment_type_id,  # Assuming type is a foreign key to Nomenclature
                "count": equipment_data.get("count"),
                "reference": equipment_data.get("reference"),
                "comment": equipment_data.get("comment"),
            }

            equipment, _created = Equipment.objects.update_or_create(
                id=equipment_id, defaults=update_values
            )
            equipments.append(equipment)
        instance.equipments.set(equipments)
        # instance.equipments.
        return super().update(instance, validated_data)

    def create(self, validated_data):
        equipments_data = validated_data.pop("equipments", [])
        media = validated_data.pop("media", [])
        if 'geom' not in validated_data or validated_data['geom'] is None:
            infrastructure = validated_data.get('infrastructure')
            print(f"INFRASTRUCTURE {infrastructure}")
            validated_data['geom'] = infrastructure.geom

        # Create the PointOperation instance
        operation = self.Meta.model.objects.create(**validated_data)

        equipments = []
        print(
            f"create operation {equipments_data}"
        )
        for equipment_data in equipments_data:
            print(
                f"PointOperationSerializer create equipement {equipment_data.keys()} {equipment_data.get('id')}"
            )
            equipment_type_id = equipment_data.get("type")
            create_values = {
                "type": equipment_type_id,  # Assuming type is a foreign key to Nomenclature
                "count": equipment_data.get("count"),
                "reference": equipment_data.get("reference"),
                "comment": equipment_data.get("comment"),
            }

            # Create the Equipment instance
            equipment = Equipment.objects.create(**create_values)
            equipments.append(equipment)

        # Optionally, you can set the equipments to the point_operation if needed
        operation.equipments.set(equipments)
        Operation.objects.filter(
            infrastructure=validated_data["infrastructure"], last=True
        ).exclude(pk=operation.id).update(last=False)

        return super().create(validated_data)

        

class LineOperationSerializer(GeoFeatureModelSerializer):
    equipments = EquipmentSerializer(many=True)

    class Meta:
        model = LineOperation
        geo_field = "geom"
        fields = [
            "id",
            "infrastructure",
            "date",
            "remark",
            "equipments",
            "media",
            # "media_id",
            "last",
            "geom",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
        }

    def update(self, instance, validated_data):
        equipments_data = validated_data.pop("equipments")
        print('validated_data', validated_data)
        # equipments = instance.equipments.all()
        equipments = []
        for equipment_data in equipments_data:
            print(
                f"equipment_data.keys() {equipment_data.keys()} {equipment_data.get('id')}"
            )
            equipment_id = (
                equipment_data.get("id") if id in equipment_data else None
            )
            equipment_type_id = equipment_data.get("type")

            update_values = {
                "type": equipment_type_id,  # Assuming type is a foreign key to Nomenclature
                "count": equipment_data.get("count"),
                "reference": equipment_data.get("reference"),
                "comment": equipment_data.get("comment"),
            }

            equipment, _created = Equipment.objects.update_or_create(
                id=equipment_id, defaults=update_values
            )
            equipments.append(equipment)
        instance.equipments.set(equipments)
        # instance.equipments.
        return super().update(instance, validated_data)

    def create(self, validated_data):
        print(f"LineOperationSerializer {validated_data}")
        equipments_data = validated_data.pop("equipments", [])
        media = validated_data.pop("media", [])
        if 'geom' not in validated_data or validated_data['geom'] is None:
            infrastructure = validated_data.get('infrastructure')
            print(f"INFRASTRUCTURE {infrastructure}")
            validated_data['geom'] = infrastructure.geom

        # Create the PointOperation instance
        print(media)
        # Create the PointOperation instance
        operation = self.Meta.model.objects.create(**validated_data)
        

        equipments = []
        print(
            f"LineOperationSerializer create line operation {equipments_data}"
        )
        for equipment_data in equipments_data:
            print(
                f"LineOperationSerializer create equipement {equipment_data.keys()} {equipment_data.get('id')}"
            )
        for equipment_data in equipments_data:
            equipment_type_id = equipment_data.get("type")
            create_values = {
                "type": equipment_type_id,  # Assuming type is a foreign key to Nomenclature
                "count": equipment_data.get("count"),
                "reference": equipment_data.get("reference"),
                "comment": equipment_data.get("comment"),
            }

            # Create the Equipment instance
            equipment = Equipment.objects.create(**create_values)
            equipments.append(equipment)

        # Optionally, you can set the equipments to the point_operation if needed
        operation.equipments.set(equipments)
        Operation.objects.filter(
            infrastructure=validated_data["infrastructure"], last=True
        ).exclude(pk=operation.id).update(last=False)

        return operation


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
    owner = NomenclatureSerializer()
    areas = GeoAreaSerializer(many=True)
    sensitive_area = SensitiveAreaSerializer(many=True)
    diagnosis = DiagnosisSerializer(many=True)
    operations = OperationSerializer(many=True)
    mortality = MortalitySimpleSerializer(many=True)

    class Meta:
        model = Infrastructure
        fields = [
            "id",
            "owner",
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


class PointSerializer(GeoFeatureModelSerializer):
    """Serializer for Point

    Used to serialize all data from Point.
    inherit from GeoAreaSerializer as contains geo data.
    """

    # Allow to display nested data
    owner = NomenclatureSerializer(read_only=True)
    areas = GeoAreaSerializer(many=True, read_only=True)
    sensitive_area = SensitiveAreaSerializer(many=True, read_only=True)
    diagnosis = DiagnosisSerializer(many=True, read_only=True)
    operations = OperationSerializer(many=True, read_only=True)
    mortality = MortalitySimpleSerializer(many=True, read_only=True)

    class Meta:
        model = Point
        geo_field = "geom"
        fields = [
            "id",
            "geom",
            "owner",
            "owner_id",
            "areas",
            # "geo_area_id",
            "sensitive_area",
            # "sensitive_area_id",
            "diagnosis",
            "operations",
            "mortality"
        ]
        # Allow to handle create/update/partial_update with nested data
        extra_kwargs = {
            "owner_id": {"source": "owner", "write_only": True},
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

    def create(self, validated_data):
        # create Point object with given coordinates
        point = Point.objects.create(**validated_data)

        try:
            # get lists of GeoArea and Sensitive_Area that intersect with Point location
            geoareas = GeoArea.objects.all().filter(
                geom__intersects=point.geom
            )
            sensitiveareas = SensitiveArea.objects.all().filter(
                geom__intersects=point.geom
            )
            # set the lists to point.geo_area and save it
            point.areas.set(geoareas)
            point.sensitive_area.set(sensitiveareas)
            point.save()

        except Exception:
            if point is not None:
                point.delete()
            msg = "Issue with attachment from new point to sensitive/geo areas. No Point created."
            logger.error(msg)
            raise APIException(msg)

        return point


class LineSerializer(GeoFeatureModelSerializer):
    """Serializer for Line

    Used to serialize all data from lines.
    inherit from GeoAreaSerializer as contains geo data.
    """

    # Allow to display nested data
    owner = NomenclatureSerializer(read_only=True)
    areas = GeoAreaSerializer(many=True, read_only=True)
    sensitive_area = SensitiveAreaSerializer(many=True, read_only=True)
    diagnosis = DiagnosisSerializer(many=True, read_only=True)
    operations = OperationSerializer(many=True, read_only=True)
    mortality = MortalitySimpleSerializer(many=True, read_only=True)

    class Meta:
        model = Line
        geo_field = "geom"
        fields = [
            "id",
            "geom",
            "owner",
            "owner_id",
            "areas",
            # "geo_area_id",
            "sensitive_area",
            # "sensitive_area_id",
            "diagnosis",
            "operations",
            "mortality"
        ]
        # Allow to handle create/update/partial_updcreateate with nested data
        extra_kwargs = {
            "owner_id": {"source": "owner", "write_only": True},
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

    def create(self, validated_data):
        # create Line object with given coordinates
        line = Line.objects.create(**validated_data)

        try:
            # get lists of GeoArea and Sensitive_Area that intersect with Line location
            geoareas = GeoArea.objects.all().filter(geom__intersects=line.geom)
            sensitiveareas = SensitiveArea.objects.all().filter(
                geom__intersects=line.geom
            )
            # set the lists to line.geo_area and save it
            line.areas.set(geoareas)
            line.sensitive_area.set(sensitiveareas)
            line.save()

        except Exception:
            if line is not None:
                line.delete()
            msg = "Issue with attachment from new Line to sensitive/geo areas. No Line created."
            logger.error(msg)
            raise APIException(msg)

        return line


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
