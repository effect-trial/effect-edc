# Generated by Django 4.2.11 on 2024-04-22 09:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("effect_subject", "0114_alter_adherence_consent_model_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="healtheconomicsevent",
            name="hospital_time",
            field=models.CharField(
                help_text="in hours and minutes (format HH:MM)",
                max_length=5,
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Expected something like 1h20m, 11h5m, etc. No spaces allowed.",
                    )
                ],
                verbose_name="How much time did you spend at the hospital or clinic?",
            ),
        ),
        migrations.AlterField(
            model_name="healtheconomicsevent",
            name="travel_time",
            field=models.CharField(
                help_text="in hours and minutes (format HH:MM)",
                max_length=5,
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Expected something like 1h20m, 11h5m, etc. No spaces allowed.",
                    )
                ],
                verbose_name="How long did it take you to reach here?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalhealtheconomicsevent",
            name="hospital_time",
            field=models.CharField(
                help_text="in hours and minutes (format HH:MM)",
                max_length=5,
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Expected something like 1h20m, 11h5m, etc. No spaces allowed.",
                    )
                ],
                verbose_name="How much time did you spend at the hospital or clinic?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalhealtheconomicsevent",
            name="travel_time",
            field=models.CharField(
                help_text="in hours and minutes (format HH:MM)",
                max_length=5,
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Expected something like 1h20m, 11h5m, etc. No spaces allowed.",
                    )
                ],
                verbose_name="How long did it take you to reach here?",
            ),
        ),
    ]
