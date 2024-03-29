# Generated by Django 3.2.8 on 2022-05-11 19:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("effect_subject", "0063_auto_20220511_1446"),
    ]

    operations = [
        migrations.RenameField(
            model_name="historicalpatienthistory",
            old_name="fluconazole_1w_prior_rando",
            new_name="flucon_1w_prior_rando",
        ),
        migrations.RenameField(
            model_name="historicalpatienthistory",
            old_name="fluconazole_days",
            new_name="flucon_days",
        ),
        migrations.RenameField(
            model_name="historicalpatienthistory",
            old_name="fluconazole_dose",
            new_name="flucon_dose",
        ),
        migrations.RenameField(
            model_name="historicalpatienthistory",
            old_name="fluconazole_dose_other",
            new_name="flucon_dose_other",
        ),
        migrations.RenameField(
            model_name="historicalpatienthistory",
            old_name="fluconazole_dose_other_reason",
            new_name="flucon_dose_other_reason",
        ),
        migrations.RenameField(
            model_name="patienthistory",
            old_name="fluconazole_1w_prior_rando",
            new_name="flucon_1w_prior_rando",
        ),
        migrations.RenameField(
            model_name="patienthistory",
            old_name="fluconazole_days",
            new_name="flucon_days",
        ),
        migrations.RenameField(
            model_name="patienthistory",
            old_name="fluconazole_dose",
            new_name="flucon_dose",
        ),
        migrations.RenameField(
            model_name="patienthistory",
            old_name="fluconazole_dose_other",
            new_name="flucon_dose_other",
        ),
        migrations.RenameField(
            model_name="patienthistory",
            old_name="fluconazole_dose_other_reason",
            new_name="flucon_dose_other_reason",
        ),
    ]
