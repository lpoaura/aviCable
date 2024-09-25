# Generated by Django 4.2.14 on 2024-08-01 09:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sinp_nomenclatures", "0001_initial"),
        ("cables", "0005_remove_diagnosis_condition_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="operation",
            name="operation_type",
        ),
        migrations.AlterField(
            model_name="equipment",
            name="type",
            field=models.ForeignKey(
                help_text="Type of equipment",
                limit_choices_to={"type__mnemonic": "equipment_type"},
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="operation_eqmt_type",
                to="sinp_nomenclatures.nomenclature",
                verbose_name="Type of equipment",
            ),
        ),
    ]