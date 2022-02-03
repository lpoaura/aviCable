# Generated by Django 4.0.1 on 2022-02-03 08:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sinp_nomenclatures", "0002_alter_source_unique_together"),
        ("mortality", "0003_alter_mortality_author"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mortality",
            name="data_source",
            field=models.ForeignKey(
                blank=True,
                help_text="Mortality data source",
                limit_choices_to={"type__mnemonic": "death_data_src"},
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="mortality_data_source",
                to="sinp_nomenclatures.item",
                verbose_name="Mortality data source",
            ),
        ),
    ]
