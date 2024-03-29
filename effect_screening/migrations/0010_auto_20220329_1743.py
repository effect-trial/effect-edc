# Generated by Django 3.2.11 on 2022-03-29 14:43

import edc_model_fields.fields.other_charfield
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("effect_screening", "0009_auto_20220111_1649"),
    ]

    operations = [
        migrations.RenameField(
            model_name="historicalsubjectscreening",
            old_name="csf_results_date",
            new_name="cm_on_csf_date",
        ),
        migrations.RenameField(
            model_name="subjectscreening",
            old_name="csf_results_date",
            new_name="cm_on_csf_date",
        ),
        migrations.RenameField(
            model_name="historicalsubjectscreening",
            old_name="csf_cm_evidence",
            new_name="cm_on_csf",
        ),
        migrations.RenameField(
            model_name="subjectscreening",
            old_name="csf_cm_evidence",
            new_name="cm_on_csf",
        ),
        migrations.AddField(
            model_name="historicalsubjectscreening",
            name="cm_on_csf_method",
            field=models.CharField(
                choices=[
                    ("india_ink", "positive microscopy with India Ink"),
                    ("culture", "culture"),
                    ("crag", "CrAg test"),
                    ("OTHER", "Other, please specify"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="If YES, by which method?",
            ),
        ),
        migrations.AddField(
            model_name="historicalsubjectscreening",
            name="cm_on_csf_method_other",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AddField(
            model_name="subjectscreening",
            name="cm_on_csf_method",
            field=models.CharField(
                choices=[
                    ("india_ink", "positive microscopy with India Ink"),
                    ("culture", "culture"),
                    ("crag", "CrAg test"),
                    ("OTHER", "Other, please specify"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="If YES, by which method?",
            ),
        ),
        migrations.AddField(
            model_name="subjectscreening",
            name="cm_on_csf_method_other",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="consent_ability",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("not_answered", "Not answered"),
                ],
                default="not_answered",
                max_length=25,
                verbose_name="Does the patient have capacity to provide informed consent for participation?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="csf_crag_value",
            field=models.CharField(
                choices=[
                    ("POS", "Positive"),
                    ("NEG", "Negative"),
                    ("PENDING", "Pending"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                help_text="If result is `pending`, report on DAY 1 / baseline visit or when available.",
                max_length=15,
                verbose_name="CSF CrAg result",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="hiv_pos",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                null=True,
                verbose_name="Is the patient CONFIRMED HIV sero-positive",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="meningitis_symptoms",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("not_answered", "Not answered"),
                ],
                default="not_answered",
                max_length=25,
                verbose_name="Has the patient had clinical symptoms/signs of symptomatic meningitis at any time since CrAg screening?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="serum_crag_value",
            field=models.CharField(
                choices=[
                    ("POS", "Positive"),
                    ("NEG", "Negative"),
                    ("not_answered", "Not answered"),
                ],
                default="not_answered",
                max_length=15,
                verbose_name="Serum/plasma CrAg result",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="willing_to_participate",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("not_answered", "Not answered"),
                ],
                default="not_answered",
                max_length=25,
                verbose_name="Is the patient willing to participate in the study if found eligible?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="consent_ability",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("not_answered", "Not answered"),
                ],
                default="not_answered",
                max_length=25,
                verbose_name="Does the patient have capacity to provide informed consent for participation?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="csf_crag_value",
            field=models.CharField(
                choices=[
                    ("POS", "Positive"),
                    ("NEG", "Negative"),
                    ("PENDING", "Pending"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                help_text="If result is `pending`, report on DAY 1 / baseline visit or when available.",
                max_length=15,
                verbose_name="CSF CrAg result",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="hiv_pos",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                null=True,
                verbose_name="Is the patient CONFIRMED HIV sero-positive",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="meningitis_symptoms",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("not_answered", "Not answered"),
                ],
                default="not_answered",
                max_length=25,
                verbose_name="Has the patient had clinical symptoms/signs of symptomatic meningitis at any time since CrAg screening?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="serum_crag_value",
            field=models.CharField(
                choices=[
                    ("POS", "Positive"),
                    ("NEG", "Negative"),
                    ("not_answered", "Not answered"),
                ],
                default="not_answered",
                max_length=15,
                verbose_name="Serum/plasma CrAg result",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="willing_to_participate",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("not_answered", "Not answered"),
                ],
                default="not_answered",
                max_length=25,
                verbose_name="Is the patient willing to participate in the study if found eligible?",
            ),
        ),
    ]
