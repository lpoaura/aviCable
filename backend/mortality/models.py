#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uuid

from cables.models import Infrastructure
from commons.models import BaseModel
from django.contrib.gis.db import models as gis_models
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from geo_area.models import GeoArea
from media.models import Media
from sinp_nomenclatures.models import Nomenclature
from species.models import Species


class Mortality(BaseModel):
    """Mortality model extending BaseModel model with metadata fields

    Describe a mortality case.
    """

    uuid = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=True, null=True, blank=True
    )
    author = models.CharField(_("Author"), max_length=100)
    geom = gis_models.PointField(srid=4326)
    date = models.DateField(
        _("Mortality observation date"), default=timezone.now
    )
    species = models.ForeignKey(
        Species,
        on_delete=models.PROTECT,
        related_name="mortality_species",
        verbose_name=_("Found dead species"),
        help_text=_("Found dead species"),
    )
    infrstr = models.ForeignKey(
        Infrastructure,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mortality",
        verbose_name=_("Infrastructure related to mortality case"),
        help_text=_("Infrastructure related to mortality case"),
    )
    areas = models.ManyToManyField(
        GeoArea,
        blank=True,
        related_name="%(class)s_areas",
        verbose_name=_("Associated Administrative and Natural Areas"),
        help_text=_("Associated Administrative and Natural Areas"),
    )
    nb_death = models.IntegerField(_("Number found dead"), default=1)
    death_cause = models.ForeignKey(
        Nomenclature,
        on_delete=models.PROTECT,
        limit_choices_to={"type__mnemonic": "cause_of_death"},
        related_name="mortality_cod",
        verbose_name=_("Cause of death"),
        help_text=_("Cause of death"),
    )
    data_source = models.ForeignKey(
        Nomenclature,
        on_delete=models.PROTECT,
        limit_choices_to={"type__mnemonic": "death_data_src"},
        null=True,
        blank=True,
        related_name="mortality_data_source",
        verbose_name=_("Mortality data source"),
        help_text=_("Mortality data source"),
    )
    data_source_url = models.URLField(
        blank=True,
        null=True,
        verbose_name=_("Mortality data source URL"),
        help_text=_("Mortality data source URL"),
    )
    media = models.ManyToManyField(
        Media,
        blank=True,
        related_name="mortality_media",
        verbose_name=_("Media related to the mortality case"),
        help_text=_("Media related to the mortality case"),
    )
    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Comment"),
        help_text=_("Comment on this mortality observations"),
    )

    class Meta:
        verbose_name = _("Mortality case")
        verbose_name_plural = _("Mortality cases")

    def __str__(self):
        return f"Mortality   : {self.species.vernacular_name} [ {self.date:%d/%m/%Y} ]"
