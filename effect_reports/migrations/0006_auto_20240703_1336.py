# Generated by Django 4.2.11 on 2024-07-03 11:36

from django.db import migrations
from edc_qareports.utils import read_unmanaged_model_sql


class Migration(migrations.Migration):

    dependencies = [
        ("effect_reports", "0005_alter_rm488serumcragdate_options_and_more"),
    ]

    operations = [
        migrations.RunSQL("drop view if exists rm488_serum_crag_date"),
        migrations.RunSQL(
            read_unmanaged_model_sql(
                "rm488_serum_crag_date.sql",
                app_name="effect_reports",
            )
        ),
    ]
