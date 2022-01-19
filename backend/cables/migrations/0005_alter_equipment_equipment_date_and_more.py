# Generated by Django 4.0.1 on 2022-01-18 13:21

import datetime

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cables", "0004_alter_equipment_equipment_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="equipment",
            name="equipment_date",
            field=models.DateTimeField(
                default=datetime.datetime(2022, 1, 18, 14, 21, 17, 240390),
                editable=False,
            ),
        ),
        migrations.AlterField(
            model_name="equipment",
            name="segment",
            field=models.ForeignKey(
                blank=True,
                help_text="Segment the equipment is installed on",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="equipment_segment",
                to="cables.segment",
                verbose_name="Segment the equipment is installed on",
            ),
        ),
    ]