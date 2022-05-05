# Generated by Django 3.2.11 on 2022-02-28 17:32

import edc_model.models.fields.other_charfield
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("effect_subject", "0020_auto_20220225_2142"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="historicalmicrobiology",
            options={
                "get_latest_by": "history_date",
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Microbiology: TB Diagnostics",
            },
        ),
        migrations.AlterModelOptions(
            name="microbiology",
            options={
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Microbiology: TB Diagnostics",
                "verbose_name_plural": "Microbiology: TB Diagnostics",
            },
        ),
        migrations.AddField(
            model_name="followup",
            name="assessment_type_other",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AddField(
            model_name="historicalfollowup",
            name="assessment_type_other",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AlterField(
            model_name="followup",
            name="assessment_type",
            field=models.CharField(
                choices=[
                    ("telephone", "Telephone"),
                    ("in_person", "In person"),
                    ("OTHER", "Other, please specify below ..."),
                ],
                max_length=15,
                verbose_name="Was this a telephone follow up or an in person visit?",
            ),
        ),
        migrations.AlterField(
            model_name="followup",
            name="info_source",
            field=models.CharField(
                choices=[
                    ("patient", "Patient"),
                    ("next_of_kin", "Next of kin"),
                    ("OTHER", "Other"),
                    ("N/A", "Not applicable (if not telephone follow-up)"),
                ],
                default="patient",
                max_length=15,
                verbose_name="If by telephone, who did you speak to?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalfollowup",
            name="assessment_type",
            field=models.CharField(
                choices=[
                    ("telephone", "Telephone"),
                    ("in_person", "In person"),
                    ("OTHER", "Other, please specify below ..."),
                ],
                max_length=15,
                verbose_name="Was this a telephone follow up or an in person visit?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalfollowup",
            name="info_source",
            field=models.CharField(
                choices=[
                    ("patient", "Patient"),
                    ("next_of_kin", "Next of kin"),
                    ("OTHER", "Other"),
                    ("N/A", "Not applicable (if not telephone follow-up)"),
                ],
                default="patient",
                max_length=15,
                verbose_name="If by telephone, who did you speak to?",
            ),
        ),
        migrations.AlterField(
            model_name="historicallpcsf",
            name="csf_culture",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("awaiting_results", "Awaiting results"),
                    ("not_done", "Not done"),
                    ("N/A", "Not applicable"),
                ],
                default="awaiting_results",
                help_text="Complete after getting the results.",
                max_length=18,
                verbose_name="CSF Result: Other organism (non-Cryptococcus)",
            ),
        ),
        migrations.AlterField(
            model_name="historicallpcsf",
            name="csf_positive",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("awaiting_results", "Awaiting results"),
                ],
                default="awaiting_results",
                max_length=18,
                verbose_name="CSF positive for cryptococcal meningitis?",
            ),
        ),
        migrations.AlterField(
            model_name="lpcsf",
            name="csf_culture",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("awaiting_results", "Awaiting results"),
                    ("not_done", "Not done"),
                    ("N/A", "Not applicable"),
                ],
                default="awaiting_results",
                help_text="Complete after getting the results.",
                max_length=18,
                verbose_name="CSF Result: Other organism (non-Cryptococcus)",
            ),
        ),
        migrations.AlterField(
            model_name="lpcsf",
            name="csf_positive",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("awaiting_results", "Awaiting results"),
                ],
                default="awaiting_results",
                max_length=18,
                verbose_name="CSF positive for cryptococcal meningitis?",
            ),
        ),
    ]
