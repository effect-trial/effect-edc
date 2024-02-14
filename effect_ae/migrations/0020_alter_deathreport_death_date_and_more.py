# Generated by Django 4.2.6 on 2023-11-14 16:14

from django.db import migrations, models
import edc_model.validators.date
import edc_protocol.validators


class Migration(migrations.Migration):
    dependencies = [
        ("effect_ae", "0019_alter_deathreport_clinical_notes_available_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="deathreport",
            name="death_date",
            field=models.DateField(
                null=True,
                validators=[
                    edc_protocol.validators.date_not_before_study_start,
                    edc_model.validators.date.date_not_future,
                ],
                verbose_name="Date of Death",
            ),
        ),
        migrations.AlterField(
            model_name="deathreport",
            name="death_datetime",
            field=models.DateTimeField(
                null=True,
                validators=[
                    edc_protocol.validators.datetime_not_before_study_start,
                    edc_model.validators.date.datetime_not_future,
                ],
                verbose_name="Date and Time of Death",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldeathreport",
            name="death_date",
            field=models.DateField(
                null=True,
                validators=[
                    edc_protocol.validators.date_not_before_study_start,
                    edc_model.validators.date.date_not_future,
                ],
                verbose_name="Date of Death",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldeathreport",
            name="death_datetime",
            field=models.DateTimeField(
                null=True,
                validators=[
                    edc_protocol.validators.datetime_not_before_study_start,
                    edc_model.validators.date.datetime_not_future,
                ],
                verbose_name="Date and Time of Death",
            ),
        ),
    ]