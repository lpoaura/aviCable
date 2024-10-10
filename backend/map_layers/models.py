from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _


class VectorLayerTheming(models.Model):
    label = models.TextField(verbose_name=_("Label"))
    min = models.FloatField(blank=True, null=True, verbose_name=_("Min"))
    max = models.FloatField(blank=True, null=True, verbose_name=_("Max"))
    numeric_value = models.FloatField(
        blank=True, null=True, verbose_name=_("Numeric value")
    )
    string_value = models.TextField(
        blank=True, null=True, verbose_name=_("String value")
    )
    style = models.JSONField(verbose_name="Style as JSON")
    condition_path = ArrayField(models.TextField(max_length=100))


class VectorLayerConfig(models.Model):
    category = models.ForeignKey(
        "sinp_nomenclatures.Nomenclature",
        on_delete=models.PROTECT,
        limit_choices_to={"type__mnemonic": "custom_gis_data_type"},
        related_name="custom_gis_data_type",
        verbose_name=_("Geographic data category"),
        help_text=_("Geographic data category"),
    )
    layer_name = models.TextField(max_length=100, verbose_name=_("layer name"))
    styles = models.ManyToManyField(
        VectorLayerTheming, verbose_name=_("Style"), related_name="config"
    )


class VectorLayerData(models.Model):
    config = models.ForeignKey(
        VectorLayerConfig,
        on_delete=models.PROTECT,
        related_name="vector_layer_data",
        verbose_name=_("Category"),
        help_text=_("Category"),
    )
    name = models.TextField(max_length=100, blank=True, null=True)
    geom = models.GeometryField(srid=4326, verbose_name="geom")
    data = models.JSONField(verbose_name="JSON Data", blank=True, null=True)

    class Meta:
        verbose_name = "Custom GIS data"
        verbose_name_plural = "Custom GIS data"

    def __str__(self):
        return self.name


class BaseLayers(models.Model):
    BASE = (
        "base",
        "Base",
    )
    OVERLAY = (
        "overlay",
        "Overlay",
    )

    LAYER_TYPES_CHOICES = [BASE, OVERLAY]
    name = models.TextField(max_length=100, verbose_name=_("Name"))
    url = models.TextField(verbose_name=_("Url"))
    attribution = models.TextField(
        max_length=256, verbose_name=_("Attribution")
    )
    default = models.BooleanField(
        default=False, verbose_name=_("Default base layer")
    )
    layer_type = models.CharField(
        max_length=50,
        choices=LAYER_TYPES_CHOICES,
        verbose_name=_("Type de couche (leaflet layer_type)"),
        default=OVERLAY[0]
    )

    class Meta:
        verbose_name = "Base layers list"
        verbose_name_plural = "Base layers list"

    def __str__(self):
        return self.name
