# Generated by Django 4.0.3 on 2022-03-16 08:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("cables", "0001_initial"),
        ("sensitive_area", "0001_initial"),
        ("contenttypes", "0002_remove_content_type_name"),
        # ("sinp_nomenclatures", "0003_rename_item_nomenclature"),
        ("geo_area", "0001_initial"),
        ("media", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="infrastructure",
            name="geo_area",
            field=models.ManyToManyField(
                blank=True,
                help_text="Associated Administrative and Natural Areas",
                related_name="%(class)s_geo_area",
                to="geo_area.geoarea",
                verbose_name="Associated Administrative and Natural Areas",
            ),
        ),
        migrations.AddField(
            model_name="infrastructure",
            name="owner",
            field=models.ForeignKey(
                help_text="Infrastructure owner",
                limit_choices_to={"type__mnemonic": "owner"},
                on_delete=django.db.models.deletion.PROTECT,
                related_name="%(class)s_owner",
                to="sinp_nomenclatures.nomenclature",
                verbose_name="Infrastructure owner",
            ),
        ),
        migrations.AddField(
            model_name="infrastructure",
            name="polymorphic_ctype",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="polymorphic_%(app_label)s.%(class)s_set+",
                to="contenttypes.contenttype",
            ),
        ),
        migrations.AddField(
            model_name="infrastructure",
            name="sensitive_area",
            field=models.ManyToManyField(
                blank=True,
                help_text="Associated Sensitivity Areas",
                related_name="%(class)s_sensitive_area",
                to="sensitive_area.sensitivearea",
                verbose_name="Associated Sensitivity Areas",
            ),
        ),
        migrations.AddField(
            model_name="infrastructure",
            name="updated_by",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="action",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="action",
            name="infrastructure",
            field=models.ForeignKey(
                help_text="Infrastructure attached with this Action",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="actions_infrastructure",
                to="cables.infrastructure",
                verbose_name="Infrastructure attached with this Action",
            ),
        ),
        migrations.AddField(
            model_name="action",
            name="media",
            field=models.ManyToManyField(
                blank=True,
                help_text="Media attached with this diagnosis",
                related_name="diagnosis_media",
                to="media.media",
                verbose_name="Media attached with this diagnosis",
            ),
        ),
        migrations.AddField(
            model_name="action",
            name="polymorphic_ctype",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="polymorphic_%(app_label)s.%(class)s_set+",
                to="contenttypes.contenttype",
            ),
        ),
        migrations.AddField(
            model_name="action",
            name="updated_by",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="operation",
            name="eqmt_type",
            field=models.ManyToManyField(
                help_text="Type of equipment",
                limit_choices_to={"type__mnemonic": "equipment_type"},
                related_name="operation_pole_eqmt_type",
                to="sinp_nomenclatures.nomenclature",
                verbose_name="Type of equipment",
            ),
        ),
        migrations.AddField(
            model_name="operation",
            name="operation_type",
            field=models.ForeignKey(
                help_text="Type of operation",
                limit_choices_to={"type__mnemonic": "operation_type"},
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="operation_type",
                to="sinp_nomenclatures.nomenclature",
                verbose_name="Type of operation",
            ),
        ),
        migrations.AddField(
            model_name="diagnosis",
            name="condition",
            field=models.ForeignKey(
                help_text="Pole condition",
                limit_choices_to={"type__mnemonic": "infrastr_condition"},
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="pole_condition",
                to="sinp_nomenclatures.nomenclature",
                verbose_name="Pole condition",
            ),
        ),
        migrations.AddField(
            model_name="diagnosis",
            name="pole_attractivity",
            field=models.ForeignKey(
                blank=True,
                help_text="Attractivity level of risk",
                limit_choices_to={"type__mnemonic": "risk_level"},
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="pole_attractivity",
                to="sinp_nomenclatures.nomenclature",
                verbose_name="Attractivity level of risk",
            ),
        ),
        migrations.AddField(
            model_name="diagnosis",
            name="pole_dangerousness",
            field=models.ForeignKey(
                blank=True,
                help_text="dangerousness level of risk",
                limit_choices_to={"type__mnemonic": "risk_level"},
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="pole_dangerousness",
                to="sinp_nomenclatures.nomenclature",
                verbose_name="dangerousness level of risk",
            ),
        ),
        migrations.AddField(
            model_name="diagnosis",
            name="pole_type",
            field=models.ManyToManyField(
                blank=True,
                help_text="Type of pole",
                limit_choices_to={"type__mnemonic": "pole_type"},
                related_name="diagnosis_pole_type",
                to="sinp_nomenclatures.nomenclature",
                verbose_name="Type of pole",
            ),
        ),
        migrations.AddField(
            model_name="diagnosis",
            name="sgmt_build_integr_risk",
            field=models.ForeignKey(
                blank=True,
                help_text="Building integration level of risk",
                limit_choices_to={"type__mnemonic": "risk_level"},
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="segment_building_integration_risk",
                to="sinp_nomenclatures.nomenclature",
                verbose_name="Building integration level of risk",
            ),
        ),
        migrations.AddField(
            model_name="diagnosis",
            name="sgmt_moving_risk",
            field=models.ForeignKey(
                blank=True,
                help_text="moving level of risk",
                limit_choices_to={"type__mnemonic": "risk_level"},
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="segment_moving_risk",
                to="sinp_nomenclatures.nomenclature",
                verbose_name="moving level of risk",
            ),
        ),
        migrations.AddField(
            model_name="diagnosis",
            name="sgmt_topo_integr_risk",
            field=models.ForeignKey(
                blank=True,
                help_text="Topological level of risk",
                limit_choices_to={"type__mnemonic": "risk_level"},
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="segment_topological_integration_risk",
                to="sinp_nomenclatures.nomenclature",
                verbose_name="topological level of risk",
            ),
        ),
        migrations.AddField(
            model_name="diagnosis",
            name="sgmt_veget_integr_risk",
            field=models.ForeignKey(
                blank=True,
                help_text="vegetation level of risk",
                limit_choices_to={"type__mnemonic": "risk_level"},
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="segment_vegetation_risk",
                to="sinp_nomenclatures.nomenclature",
                verbose_name="vegetation level of risk",
            ),
        ),
    ]
