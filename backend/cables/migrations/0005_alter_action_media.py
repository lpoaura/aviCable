# Generated by Django 4.0.1 on 2022-03-01 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("media", "0001_initial"),
        ("cables", "0004_alter_diagnosis_pole_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="action",
            name="media",
            field=models.ManyToManyField(
                help_text="Media attached with this visit",
                related_name="visit_media",
                to="media.Media",
                verbose_name="Media attached with this visit",
            ),
        ),
    ]
