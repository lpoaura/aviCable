# Generated by Django 4.2.7 on 2023-12-13 11:50

import django.contrib.gis.db.models.fields
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("sinp_nomenclatures", "0001_initial"),
        ("cables", "0001_initial"),
        ("media", "0002_alter_media_storage"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("species", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Mortality",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("timestamp_create", models.DateTimeField(auto_now_add=True)),
                ("timestamp_update", models.DateTimeField(auto_now=True)),
                (
                    "author",
                    models.CharField(max_length=100, verbose_name="Author"),
                ),
                (
                    "geom",
                    django.contrib.gis.db.models.fields.PointField(srid=4326),
                ),
                (
                    "date",
                    models.DateField(
                        default=django.utils.timezone.now,
                        verbose_name="Mortality observation date",
                    ),
                ),
                (
                    "nb_death",
                    models.IntegerField(
                        default=1, verbose_name="Number found dead"
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "data_source",
                    models.ForeignKey(
                        blank=True,
                        help_text="Mortality data source",
                        limit_choices_to={"type__mnemonic": "death_data_src"},
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="mortality_data_source",
                        to="sinp_nomenclatures.nomenclature",
                        verbose_name="Mortality data source",
                    ),
                ),
                (
                    "death_cause",
                    models.ForeignKey(
                        help_text="Cause of death",
                        limit_choices_to={"type__mnemonic": "cause_of_death"},
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="mortality_cod",
                        to="sinp_nomenclatures.nomenclature",
                        verbose_name="Cause of death",
                    ),
                ),
                (
                    "infrstr",
                    models.ForeignKey(
                        blank=True,
                        help_text="Infrastructure related to mortality case",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="mortality_infrstr",
                        to="cables.infrastructure",
                        verbose_name="Infrastructure related to mortality case",
                    ),
                ),
                (
                    "media",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Media related to the mortality case",
                        related_name="mortality_media",
                        to="media.media",
                        verbose_name="Media related to the mortality case",
                    ),
                ),
                (
                    "species",
                    models.ForeignKey(
                        help_text="Found dead species",
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="mortality_species",
                        to="species.species",
                        verbose_name="Found dead species",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Mortality case",
                "verbose_name_plural": "Mortality cases",
            },
        ),
    ]
