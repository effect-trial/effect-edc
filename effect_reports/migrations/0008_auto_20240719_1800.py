# Generated by Django 4.2.11 on 2024-07-19 16:00

from django.db import migrations
from edc_qareports.utils import read_unmanaged_model_sql


class Migration(migrations.Migration):

    dependencies = [
        ("effect_reports", "0007_rm488consented"),
    ]

    operations = [
        migrations.RunSQL(
            read_unmanaged_model_sql(
                "rm488_consented.sql",
                app_name="effect_reports",
            )
        ),
    ]
