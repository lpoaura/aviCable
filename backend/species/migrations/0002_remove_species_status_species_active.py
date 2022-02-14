# Generated by Django 4.0.1 on 2022-02-03 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("species", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="species",
            name="status",
        ),
        migrations.AddField(
            model_name="species",
            name="active",
            field=models.BooleanField(default=True, verbose_name="Active"),
        ),
    ]