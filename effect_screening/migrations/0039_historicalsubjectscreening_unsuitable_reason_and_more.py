# Generated by Django 4.2.6 on 2024-03-12 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("effect_screening", "0038_populate_safe_save_id_values"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalsubjectscreening",
            name="unsuitable_reason",
            field=models.CharField(
                choices=[
                    ("active_substance_addiction", "Active substance addiction"),
                    ("dead", "Died prior to screening being completed"),
                    (
                        "unable_to_contact",
                        "No reliable means of communicating with/ contacting/ following up",
                    ),
                    (
                        "relocated",
                        "Relocated or planning to relocate within next 14 days to non-EFFECT site",
                    ),
                    ("OTHER", "Other, please specify below ..."),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=30,
                verbose_name="If YES, reason not suitable for the study",
            ),
        ),
        migrations.AddField(
            model_name="historicalsubjectscreening",
            name="unsuitable_reason_other",
            field=models.TextField(
                blank=True,
                max_length=150,
                null=True,
                verbose_name="If other reason unsuitable, please specify ...",
            ),
        ),
        migrations.AddField(
            model_name="subjectscreening",
            name="unsuitable_reason",
            field=models.CharField(
                choices=[
                    ("active_substance_addiction", "Active substance addiction"),
                    ("dead", "Died prior to screening being completed"),
                    (
                        "unable_to_contact",
                        "No reliable means of communicating with/ contacting/ following up",
                    ),
                    (
                        "relocated",
                        "Relocated or planning to relocate within next 14 days to non-EFFECT site",
                    ),
                    ("OTHER", "Other, please specify below ..."),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=30,
                verbose_name="If YES, reason not suitable for the study",
            ),
        ),
        migrations.AddField(
            model_name="subjectscreening",
            name="unsuitable_reason_other",
            field=models.TextField(
                blank=True,
                max_length=150,
                null=True,
                verbose_name="If other reason unsuitable, please specify ...",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="unsuitable_for_study",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("not_evaluated", "Not evaluated")],
                default="not_evaluated",
                help_text="If YES, patient NOT eligible, please specify reason below ...",
                max_length=15,
                verbose_name="Is there any other reason the patient is deemed to not be suitable for the study?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="unsuitable_for_study",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("not_evaluated", "Not evaluated")],
                default="not_evaluated",
                help_text="If YES, patient NOT eligible, please specify reason below ...",
                max_length=15,
                verbose_name="Is there any other reason the patient is deemed to not be suitable for the study?",
            ),
        ),
    ]
