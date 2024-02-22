#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""These application models are using nomenclature Items 'cf. sinp_nomenclatures' module

    Item works like dictionnary term used to configure related application. Each Item is related to a Type, itself related to a Source. An application can authorize for a specific field to complete it with list of all Item terms with a defined Type (selected by Type mnemonic field). This allows to set up authorized entries for these field through database entries, not through hardcoded way,making application more flexible and more maintanable.
"""
import datetime
from uuid import uuid4

from commons.models import BaseModel
from django.contrib.gis.db import models as gis_models
from django.db import models
from django.utils.translation import gettext_lazy as _
from geo_area.models import GeoArea
from media.models import Media
from polymorphic.models import PolymorphicModel
from sensitive_area.models import SensitiveArea
from sinp_nomenclatures.models import Nomenclature


class Infrastructure(BaseModel, PolymorphicModel):
    """Common shared infrastructure model with metadata fields, inheriting from BaseModel and PolymorphicModel

    This model define generic information relative to an infrastructure such as electrical pole/pylon or power line segment.
    Model defined as PolymorphicModel: all specific infrastructures classes (e.g. Point, Line) will inherit from this class.
    uuid is a unique identifier (not primary key). It can be used as data identifier in case of
    data gathered from various origin (e.g. populating data from various DB)
    """

    uuid = models.UUIDField(
        default=uuid4,
        unique=True,
        editable=False,
        verbose_name=_("Identifiant unique"),
    )
    owner = models.ForeignKey(
        Nomenclature,
        on_delete=models.PROTECT,
        limit_choices_to={"type__mnemonic": "owner"},
        related_name="%(class)s_owner",
        verbose_name=_("Infrastructure owner"),
        help_text=_("Infrastructure owner"),
    )
    geo_area = models.ManyToManyField(
        GeoArea,
        blank=True,
        related_name="%(class)s_geo_area",
        verbose_name=_("Associated Administrative and Natural Areas"),
        help_text=_("Associated Administrative and Natural Areas"),
    )
    sensitive_area = models.ManyToManyField(
        SensitiveArea,
        blank=True,
        related_name="%(class)s_sensitive_area",
        verbose_name=_("Associated Sensitivity Areas"),
        help_text=_("Associated Sensitivity Areas"),
    )

    class Meta:
        ordering = ["-id"]


class Point(Infrastructure):
    """Point model inheriting from InfrastructureModel

    Used for a point infrastructure like an electric pole/pylon.
    """

    geom = gis_models.PointField(srid=4326)

    def __str__(self):
        return f"Point {self.pk}"


class Line(Infrastructure):
    """Line model inheriting InfrastructureModel

    Used for a point infrastructure a power line segment.
    """

    geom = gis_models.LineStringField(null=True, blank=True, srid=4326)

    def __str__(self):
        return f"Line {self.pk}"


class Action(BaseModel):
    """Common shared Action model inheriting from BaseModel

    This model define generic information relative to an action on an infrastructure such as diagnosis or operation.
    Model defined as PolymorphicModel: all specific actions classes (e.g. Diagnosis, Operation) will inherit from this class.
    uuid is a unique identifier (not primary key). It can be used as data identifier in case of
    data gathered from various origin (e.g. populating data from various DB)
    """

    uuid = models.UUIDField(
        default=uuid4,
        unique=True,
        editable=False,
        verbose_name=_("unique Id"),
    )

    date = models.DateField(_("Date"), default=datetime.date.today)
    remark = models.TextField(_("Remarks"), blank=True, null=True)

    # Field usefull for child (Diagnosis or Operation) creation
    # If Diagnosis or Operation already exists for the infrastructure, the new item received True # as last record, and old ones receive False.
    last = models.BooleanField(
        _("Last record"),
        default=True,
    )

    class Meta:
        ordering = ["-date"]
        abstract = True


class Diagnosis(Action):
    """Diagnosis model inheriting ActionModel

    Stand for a description of an infrastructure. Severa description may exist for the same infrastructure, with informations updated (at the occasion of new diagnosis). This allow to maintain an history of infrastructure diagnosis.
    """

    infrastructure = models.ForeignKey(
        Infrastructure,
        on_delete=models.CASCADE,
        related_name="diagnosis",
        verbose_name=_("Infrastructure attached with this Action"),
        help_text=_("Infrastructure attached with this Action"),
    )
    media = models.ManyToManyField(
        Media,
        blank=True,
        related_name="diagnosis_media",
        verbose_name=_("Media attached with this diagnosis"),
        help_text=_("Media attached with this diagnosis"),
        related_query_name="diagnosis",
    )
    neutralized = models.BooleanField(_("Neutralized"), default=False)
    condition = models.ForeignKey(
        Nomenclature,
        on_delete=models.PROTECT,
        null=True,
        limit_choices_to={"type__mnemonic": "infrastr_condition"},
        related_name="pole_condition",
        verbose_name=_("Pole condition"),
        help_text=_("Pole condition"),
    )
    isolation_advice = models.BooleanField(
        _("To be insulated"),
        default=False,
    )
    dissuasion_advice = models.BooleanField(
        _("Discourage"),
        default=False,
    )
    attraction_advice = models.BooleanField(
        _("Providing incentives"),
        default=False,
    )
    change_advice = models.BooleanField(
        _("Change arming"),
        default=False,
    )
    technical_proposal = models.TextField(
        _("Technical proposal"), blank=True, null=True
    )
    pole_type = models.ManyToManyField(
        Nomenclature,
        blank=True,
        limit_choices_to={"type__mnemonic": "pole_type"},
        related_name="diagnosis_pole_type",
        verbose_name=_("Type of pole"),
        help_text=_("Type of pole"),
    )
    pole_attractivity = models.ForeignKey(
        Nomenclature,
        on_delete=models.PROTECT,
        limit_choices_to={"type__mnemonic": "risk_level"},
        blank=True,
        null=True,
        related_name="pole_attractivity",
        verbose_name=_("Attractivity level of risk"),
        help_text=_("Attractivity level of risk"),
    )
    pole_dangerousness = models.ForeignKey(
        Nomenclature,
        on_delete=models.PROTECT,
        limit_choices_to={"type__mnemonic": "risk_level"},
        blank=True,
        null=True,
        related_name="pole_dangerousness",
        verbose_name=_("dangerousness level of risk"),
        help_text=_("dangerousness level of risk"),
    )
    sgmt_build_integr_risk = models.ForeignKey(
        Nomenclature,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        limit_choices_to={"type__mnemonic": "risk_level"},
        related_name="segment_building_integration_risk",
        verbose_name=_("Building integration level of risk"),
        help_text=_("Building integration level of risk"),
    )
    sgmt_moving_risk = models.ForeignKey(
        Nomenclature,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        limit_choices_to={"type__mnemonic": "risk_level"},
        related_name="segment_moving_risk",
        verbose_name=_("moving level of risk"),
        help_text=_("moving level of risk"),
    )
    sgmt_topo_integr_risk = models.ForeignKey(
        Nomenclature,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        limit_choices_to={"type__mnemonic": "risk_level"},
        related_name="segment_topological_integration_risk",
        verbose_name=_("topological level of risk"),
        help_text=_("Topological level of risk"),
    )
    sgmt_veget_integr_risk = models.ForeignKey(
        Nomenclature,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        limit_choices_to={"type__mnemonic": "risk_level"},
        related_name="segment_vegetation_risk",
        verbose_name=_("vegetation level of risk"),
        help_text=_("vegetation level of risk"),
    )

    class Meta:
        verbose_name_plural = _("Diagnosis")


class Equipment(BaseModel):
    uuid = models.UUIDField(
        default=uuid4,
        unique=True,
        editable=False,
        verbose_name=_("unique Id"),
    )
    type = models.ForeignKey(
        Nomenclature,
        limit_choices_to={"type__mnemonic": "equipment_type"},
        related_name="operation_pole_eqmt_type",
        verbose_name=_("Type of equipment"),
        help_text=_("Type of equipment"),
        on_delete=models.CASCADE,
    )
    count = models.PositiveIntegerField(_("Number of equipments"), default=1)
    reference = models.TextField(
        _("Equipment model reference"), blank=True, null=True
    )
    comment = models.TextField(_("Comments"), blank=True, null=True)


class Operation(Action, PolymorphicModel):
    """Operation model inheriting ActionModel

    Define an operation on an infrastructure.
    """

    infrastructure = models.ForeignKey(
        Infrastructure,
        on_delete=models.CASCADE,
        related_name="operations",
        verbose_name=_("Infrastructure attached with this Action"),
        help_text=_("Infrastructure attached with this Action"),
    )
    media = models.ManyToManyField(
        Media,
        blank=True,
        related_name="operations_media",
        verbose_name=_("Media attached with this diagnosis"),
        help_text=_("Media attached with this diagnosis"),
        related_query_name="operations",
    )
    operation_type = models.ForeignKey(
        Nomenclature,
        on_delete=models.PROTECT,
        limit_choices_to={"type__mnemonic": "operation_type"},
        related_name="operation_type",
        verbose_name=_("Type of operation"),
        help_text=_("Type of operation"),
        # TODO to be removed
        null=True,
    )
    equipments = models.ManyToManyField(
        Equipment,
        related_name="equipment",
        verbose_name=_("Equipments"),
        help_text=_("Equipements"),
        related_query_name="operations",
        blank=True,
    )


class PointOperation(Operation):
    """Point model Operation model

    Used for a support operations.
    """

    geom = gis_models.PointField(srid=4326)

    def __str__(self):
        return f"PointOperation object ({self.pk}) {dir(self)}"


class LineOperation(Operation):
    """Line model inheriting Operation model

    Used for a line operation a power line segment.
    """

    geom = gis_models.LineStringField(null=True, blank=True, srid=4326)

    def __str__(self):
        return f"LineOperation ({self.pk})"
