# Generated by Django 3.2.13 on 2022-05-27 11:51

import edc_model.models.fields.duration
import edc_model.validators.date
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("effect_screening", "0021_auto_20220516_1231"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalsubjectscreening",
            name="hiv_dx_ago",
            field=edc_model.models.fields.duration.DurationYMDField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="historicalsubjectscreening",
            name="hiv_dx_date",
            field=models.DateField(
                blank=True,
                help_text="If possible, provide the exact date here instead of estimating above.",
                null=True,
                validators=[edc_model.validators.date.date_not_future],
                verbose_name="Date patient diagnosed",
            ),
        ),
        migrations.AddField(
            model_name="historicalsubjectscreening",
            name="hiv_dx_date_is_estimated",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                editable=False,
                max_length=15,
                verbose_name="Was the diagnosis date estimated?",
            ),
        ),
        migrations.AddField(
            model_name="historicalsubjectscreening",
            name="hiv_dx_estimated_date",
            field=models.DateField(
                editable=False,
                help_text="Calculated based on response to `hiv_dx_ago`",
                null=True,
                verbose_name="Estimated diagnoses date",
            ),
        ),
        migrations.AddField(
            model_name="subjectscreening",
            name="hiv_dx_ago",
            field=edc_model.models.fields.duration.DurationYMDField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="subjectscreening",
            name="hiv_dx_date",
            field=models.DateField(
                blank=True,
                help_text="If possible, provide the exact date here instead of estimating above.",
                null=True,
                validators=[edc_model.validators.date.date_not_future],
                verbose_name="Date patient diagnosed",
            ),
        ),
        migrations.AddField(
            model_name="subjectscreening",
            name="hiv_dx_date_is_estimated",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                editable=False,
                max_length=15,
                verbose_name="Was the diagnosis date estimated?",
            ),
        ),
        migrations.AddField(
            model_name="subjectscreening",
            name="hiv_dx_estimated_date",
            field=models.DateField(
                editable=False,
                help_text="Calculated based on response to `hiv_dx_ago`",
                null=True,
                verbose_name="Estimated diagnoses date",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="hiv_pos",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                null=True,
                verbose_name="Is the patient CONFIRMED HIV sero-positive?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="hiv_pos",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                null=True,
                verbose_name="Is the patient CONFIRMED HIV sero-positive?",
            ),
        ),
    ]
