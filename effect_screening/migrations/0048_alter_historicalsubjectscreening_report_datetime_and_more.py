# Generated by Django 4.2.11 on 2024-05-20 11:22

from django.db import migrations, models
import edc_model.validators.date
import edc_protocol.validators
import edc_utils.date


class Migration(migrations.Migration):

    dependencies = [
        ("effect_screening", "0047_alter_historicalsubjectscreening_lp_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="report_datetime",
            field=models.DateTimeField(
                default=edc_utils.date.get_utcnow,
                help_text="Date and time of report.",
                validators=[
                    edc_protocol.validators.datetime_not_before_study_start,
                    edc_model.validators.date.datetime_not_future,
                ],
                verbose_name="Report Date and Time",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="report_datetime",
            field=models.DateTimeField(
                default=edc_utils.date.get_utcnow,
                help_text="Date and time of report.",
                validators=[
                    edc_protocol.validators.datetime_not_before_study_start,
                    edc_model.validators.date.datetime_not_future,
                ],
                verbose_name="Report Date and Time",
            ),
        ),
    ]
