# Generated by Django 4.2.11 on 2024-04-18 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "effect_screening",
            "0043_alter_historicalsubjectscreening_unsuitable_reason_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="unsuitable_reason",
            field=models.CharField(
                choices=[
                    ("active_substance_addiction", "Active substance addiction"),
                    ("dead", "Died prior to screening being completed"),
                    ("g4_thrombocytopenia", "Known to have DAIDS grade 4 thrombocytopenia"),
                    ("g4_neutropaenia", "Known to have DAIDS grade 4 neutropaenia"),
                    ("g4_raised_creatinine", "Known to have DAIDS grade 4 raised creatinine"),
                    (
                        "no_reliable_followup",
                        "No reliable means of communicating with/following up",
                    ),
                    (
                        "relocated",
                        "Relocated or planning to relocate within next 14 days to non-EFFECT site",
                    ),
                    ("unable_to_contact", "Unable to contact patient for screening"),
                    ("OTHER", "Other, please specify below ..."),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=30,
                verbose_name="If YES, reason not suitable for the study",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="unsuitable_reason",
            field=models.CharField(
                choices=[
                    ("active_substance_addiction", "Active substance addiction"),
                    ("dead", "Died prior to screening being completed"),
                    ("g4_thrombocytopenia", "Known to have DAIDS grade 4 thrombocytopenia"),
                    ("g4_neutropaenia", "Known to have DAIDS grade 4 neutropaenia"),
                    ("g4_raised_creatinine", "Known to have DAIDS grade 4 raised creatinine"),
                    (
                        "no_reliable_followup",
                        "No reliable means of communicating with/following up",
                    ),
                    (
                        "relocated",
                        "Relocated or planning to relocate within next 14 days to non-EFFECT site",
                    ),
                    ("unable_to_contact", "Unable to contact patient for screening"),
                    ("OTHER", "Other, please specify below ..."),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=30,
                verbose_name="If YES, reason not suitable for the study",
            ),
        ),
    ]
