# Generated by Django 3.2.9 on 2021-11-19 18:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("effect_screening", "0005_auto_20211119_2024"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalsubjectscreening",
            name="csf_results_date",
            field=models.DateField(
                blank=True, null=True, verbose_name="Date results expected (estimate)"
            ),
        ),
        migrations.AddField(
            model_name="subjectscreening",
            name="csf_results_date",
            field=models.DateField(
                blank=True, null=True, verbose_name="Date results expected (estimate)"
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="contraindicated_meds",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("not_answered", "Not answered")],
                default="not_answered",
                help_text="Refer to the protocol for a complete list",
                max_length=25,
                verbose_name="Is the patient taking any contraindicated concomitant medications?",
            ),
        ),
        migrations.AlterField(
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
                help_text="At any time between the CrAg test and screening for eligibility. <BR>If results on tests on CSF are `pending`, report on DAY 1 / baseline visit or when available.",
                max_length=25,
                verbose_name="Any other evidence of CM on CSF?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="meningitis_symptoms",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("not_answered", "Not answered")],
                default="not_answered",
                max_length=25,
                verbose_name="Has the patient had clinical symptoms/ signs of symptomatic meningitis at any time since CrAg screening?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="pregnant_or_bf",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("N/A", "Not Applicable: e.g. male or post-menopausal"),
                    ("not_answered", "Not answered"),
                ],
                default="not_answered",
                max_length=15,
                verbose_name="Is the patient pregnant or breastfeeding?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="contraindicated_meds",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("not_answered", "Not answered")],
                default="not_answered",
                help_text="Refer to the protocol for a complete list",
                max_length=25,
                verbose_name="Is the patient taking any contraindicated concomitant medications?",
            ),
        ),
        migrations.AlterField(
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
                help_text="At any time between the CrAg test and screening for eligibility. <BR>If results on tests on CSF are `pending`, report on DAY 1 / baseline visit or when available.",
                max_length=25,
                verbose_name="Any other evidence of CM on CSF?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="meningitis_symptoms",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("not_answered", "Not answered")],
                default="not_answered",
                max_length=25,
                verbose_name="Has the patient had clinical symptoms/ signs of symptomatic meningitis at any time since CrAg screening?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="pregnant_or_bf",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("N/A", "Not Applicable: e.g. male or post-menopausal"),
                    ("not_answered", "Not answered"),
                ],
                default="not_answered",
                max_length=15,
                verbose_name="Is the patient pregnant or breastfeeding?",
            ),
        ),
    ]
