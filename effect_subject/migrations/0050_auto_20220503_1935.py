# Generated by Django 3.2.11 on 2022-05-03 16:35

import edc_model.models.fields.other_charfield
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("effect_subject", "0049_auto_20220503_1933"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalpatienttreatment",
            name="antibiotics_given_other",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AlterField(
            model_name="historicalpatienttreatment",
            name="cm_tx",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=15,
                verbose_name="Cryptococcal meningitis treatment administered?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalpatienttreatment",
            name="steroids",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Were steroids administered to the patient?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalpatienttreatment",
            name="steroids_given",
            field=models.CharField(
                choices=[
                    ("oral_prednisolone", "Oral prednisolone"),
                    ("iv_dexamethasone", "IV Dexamethasone"),
                    ("OTHER", "Other, please specify below ..."),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=35,
                verbose_name="If YES, which steroids?",
            ),
        ),
        migrations.AlterField(
            model_name="patienttreatment",
            name="antibiotics_given_other",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AlterField(
            model_name="patienttreatment",
            name="cm_tx",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=15,
                verbose_name="Cryptococcal meningitis treatment administered?",
            ),
        ),
        migrations.AlterField(
            model_name="patienttreatment",
            name="steroids",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Were steroids administered to the patient?",
            ),
        ),
        migrations.AlterField(
            model_name="patienttreatment",
            name="steroids_given",
            field=models.CharField(
                choices=[
                    ("oral_prednisolone", "Oral prednisolone"),
                    ("iv_dexamethasone", "IV Dexamethasone"),
                    ("OTHER", "Other, please specify below ..."),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=35,
                verbose_name="If YES, which steroids?",
            ),
        ),
    ]