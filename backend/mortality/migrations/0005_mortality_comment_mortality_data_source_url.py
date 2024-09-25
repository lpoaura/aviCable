# Generated by Django 4.2.14 on 2024-09-19 09:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mortality", "0004_mortality_alter_uuid"),
    ]

    operations = [
        migrations.AddField(
            model_name="mortality",
            name="comment",
            field=models.TextField(
                blank=True,
                help_text="Comment on this mortality observations",
                null=True,
                verbose_name="Comment",
            ),
        ),
        migrations.AddField(
            model_name="mortality",
            name="data_source_url",
            field=models.URLField(
                blank=True,
                help_text="Mortality data source URL",
                null=True,
                verbose_name="Mortality data source URL",
            ),
        ),
    ]