# Generated by Django 5.1.3 on 2024-11-28 18:27

import edc_utils.date
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("effect_reports", "0007_update_rm792_views"),
    ]

    operations = [
        migrations.AlterField(
            model_name="serumcragdate",
            name="created",
            field=models.DateTimeField(default=edc_utils.date.get_utcnow),
        ),
    ]
