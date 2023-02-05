# Generated by Django 3.2 on 2022-09-15 14:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("effect_screening", "0025_auto_20220711_1230"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="cm_in_csf",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("PENDING", "Pending results"),
                    ("not_tested", "No further testing done"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                help_text="At any time between the CrAg test and screening for eligibility. <BR>If results on tests on CSF are `pending`, report on DAY 1 / baseline visit or when available.",
                max_length=25,
                verbose_name="Was CM confirmed in CSF by any other method?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="cm_in_csf_method",
            field=models.CharField(
                choices=[
                    ("india_ink", "Positive microscopy with India Ink or other method"),
                    ("culture", "Positive culture"),
                    ("OTHER", "Other, please specify"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="If YES, by which method?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="cm_in_csf",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("PENDING", "Pending results"),
                    ("not_tested", "No further testing done"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                help_text="At any time between the CrAg test and screening for eligibility. <BR>If results on tests on CSF are `pending`, report on DAY 1 / baseline visit or when available.",
                max_length=25,
                verbose_name="Was CM confirmed in CSF by any other method?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="cm_in_csf_method",
            field=models.CharField(
                choices=[
                    ("india_ink", "Positive microscopy with India Ink or other method"),
                    ("culture", "Positive culture"),
                    ("OTHER", "Other, please specify"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="If YES, by which method?",
            ),
        ),
    ]
