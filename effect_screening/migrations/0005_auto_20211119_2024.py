# Generated by Django 3.2.9 on 2021-11-19 17:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("effect_screening", "0004_auto_20211119_1937"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicalsubjectscreening",
            name="csf_cm_value",
        ),
        migrations.RemoveField(
            model_name="subjectscreening",
            name="csf_cm_value",
        ),
        migrations.AddField(
            model_name="historicalsubjectscreening",
            name="csf_cm_evidence",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("PENDING", "Pending results"),
                    ("not_tested", "Additional testing not done"),
                    ("N/A", "Not applicable"),
                    ("not_answered", "Not answered"),
                ],
                default="not_answered",
                max_length=25,
                verbose_name="Any other evidence of CM on CSF?",
            ),
        ),
        migrations.AddField(
            model_name="subjectscreening",
            name="csf_cm_evidence",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("PENDING", "Pending results"),
                    ("not_tested", "Additional testing not done"),
                    ("N/A", "Not applicable"),
                    ("not_answered", "Not answered"),
                ],
                default="not_answered",
                max_length=25,
                verbose_name="Any other evidence of CM on CSF?",
            ),
        ),
    ]
