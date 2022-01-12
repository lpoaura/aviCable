# Generated by Django 4.0.1 on 2022-01-12 13:56

import django.contrib.gis.db.models.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("sinp_nomenclatures", "0002_alter_source_unique_together"),
    ]

    operations = [
        migrations.CreateModel(
            name="GeoArea",
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
                (
                    "geom",
                    django.contrib.gis.db.models.fields.PolygonField(
                        blank=True, null=True, srid=4326
                    ),
                ),
                (
                    "name",
                    models.ForeignKey(
                        help_text="Name of the geographical area",
                        limit_choices_to={"type__mnemonic": "geoarea_name"},
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="geoarea_name",
                        to="sinp_nomenclatures.item",
                        verbose_name="Name of the geographical area",
                    ),
                ),
            ],
            options={
                "db_table": "geo_area",
            },
        ),
    ]
