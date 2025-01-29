# Generated by Django 5.1.3 on 2025-01-23 11:46

from django.db import migrations
from edc_qareports.utils import read_unmanaged_model_sql


class Migration(migrations.Migration):

    dependencies = [
        ("effect_reports", "0011_alter_baselinevldiscrepancy_options_and_more"),
    ]

    operations = [
        migrations.RunSQL("drop view if exists rm792_kw_in_current_sx_other"),
        migrations.RunSQL(
            read_unmanaged_model_sql(
                "rm792_kw_in_current_sx_other.sql",
                app_name="effect_reports",
            )
        ),
        migrations.RunSQL("drop view if exists rm792_kw_in_current_sx_gte_g3_other"),
        migrations.RunSQL(
            read_unmanaged_model_sql(
                "rm792_kw_in_current_sx_gte_g3_other.sql",
                app_name="effect_reports",
            )
        ),
        migrations.RunSQL("drop view if exists rm792_si_sx_list_candidates"),
        migrations.RunSQL(
            read_unmanaged_model_sql(
                "rm792_si_sx_list_candidates.sql",
                app_name="effect_reports",
            )
        ),
    ]
