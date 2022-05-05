# Generated by Django 3.2.11 on 2022-05-01 12:55

from django.db import migrations, models

import effect_subject.models.subject_visit


class Migration(migrations.Migration):

    dependencies = [
        ("effect_subject", "0047_auto_20220501_1554"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="subjectvisit",
            managers=[
                ("on_site", effect_subject.models.subject_visit.CurrentSiteManager()),
                ("objects", effect_subject.models.subject_visit.VisitModelManager()),
            ],
        ),
        migrations.AddField(
            model_name="historicalsubjectvisit",
            name="document_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default="COMPLETE",
                help_text="If some data is still pending, flag as incomplete",
                max_length=25,
                verbose_name="Document status",
            ),
        ),
        migrations.AddField(
            model_name="subjectvisit",
            name="document_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default="COMPLETE",
                help_text="If some data is still pending, flag as incomplete",
                max_length=25,
                verbose_name="Document status",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectvisit",
            name="assessment_type",
            field=models.CharField(
                choices=[
                    ("telephone", "Telephone"),
                    ("in_person", "In person"),
                    ("N/A", "Not applicable (if missed)"),
                    ("OTHER", "Other, please specify below ..."),
                ],
                max_length=15,
                verbose_name="Was this a telephone or an in person visit?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectvisit",
            name="assessment_who",
            field=models.CharField(
                choices=[
                    ("patient", "Patient"),
                    ("next_of_kin", "Next of kin"),
                    ("N/A", "Not applicable (if missed)"),
                    ("OTHER", "Other, please specify below ..."),
                ],
                max_length=15,
                verbose_name="Who did you speak to?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectvisit",
            name="hospitalized",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("unknown", "Unknown"),
                    ("N/A", "Not applicable (if missed)"),
                ],
                default="N/A",
                help_text="If YES, complete AE Initial report.",
                max_length=15,
                verbose_name="Has the patient been hospitalized since the last assessment?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectvisit",
            name="survival_status",
            field=models.CharField(
                choices=[
                    ("alive", "Alive"),
                    ("dead", "Deceased"),
                    ("unknown", "Unknown"),
                    ("N/A", "Not applicable (if missed)"),
                ],
                default="alive",
                help_text="If YES, submit Death report",
                max_length=10,
                null=True,
                verbose_name="Participant's survival status",
            ),
        ),
        migrations.AlterField(
            model_name="subjectvisit",
            name="assessment_type",
            field=models.CharField(
                choices=[
                    ("telephone", "Telephone"),
                    ("in_person", "In person"),
                    ("N/A", "Not applicable (if missed)"),
                    ("OTHER", "Other, please specify below ..."),
                ],
                max_length=15,
                verbose_name="Was this a telephone or an in person visit?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectvisit",
            name="assessment_who",
            field=models.CharField(
                choices=[
                    ("patient", "Patient"),
                    ("next_of_kin", "Next of kin"),
                    ("N/A", "Not applicable (if missed)"),
                    ("OTHER", "Other, please specify below ..."),
                ],
                max_length=15,
                verbose_name="Who did you speak to?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectvisit",
            name="hospitalized",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("unknown", "Unknown"),
                    ("N/A", "Not applicable (if missed)"),
                ],
                default="N/A",
                help_text="If YES, complete AE Initial report.",
                max_length=15,
                verbose_name="Has the patient been hospitalized since the last assessment?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectvisit",
            name="survival_status",
            field=models.CharField(
                choices=[
                    ("alive", "Alive"),
                    ("dead", "Deceased"),
                    ("unknown", "Unknown"),
                    ("N/A", "Not applicable (if missed)"),
                ],
                default="alive",
                help_text="If YES, submit Death report",
                max_length=10,
                null=True,
                verbose_name="Participant's survival status",
            ),
        ),
    ]
