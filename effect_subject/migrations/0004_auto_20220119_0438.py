# Generated by Django 3.2.11 on 2022-01-19 01:38

import django.core.validators
import edc_model.models.fields.other_charfield
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("effect_subject", "0003_auto_20220111_1649"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalstudytreatment",
            name="antibiotics_other",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other antibiotics, please specify ...",
            ),
        ),
        migrations.AddField(
            model_name="historicalstudytreatment",
            name="tb_tx_given_other",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other TB treatment given, please specify ...",
            ),
        ),
        migrations.AddField(
            model_name="studytreatment",
            name="antibiotics_other",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other antibiotics, please specify ...",
            ),
        ),
        migrations.AddField(
            model_name="studytreatment",
            name="tb_tx_given_other",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other TB treatment given, please specify ...",
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
                    ("N/A", "Not applicable (in person visit)"),
                ],
                default="patient",
                max_length=15,
                verbose_name="If by telephone, who did you speak to?",
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
                    ("N/A", "Not applicable (in person visit)"),
                ],
                default="patient",
                max_length=15,
                verbose_name="If by telephone, who did you speak to?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalstudytreatment",
            name="cm_confirmed",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                max_length=15,
                verbose_name="Cryptococcal meningitis confirmed?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalstudytreatment",
            name="cm_tx_administered",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                max_length=15,
                verbose_name="Cryptococcal meningitis treatment administered?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalstudytreatment",
            name="cm_tx_given_other",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other CM treatment given, please specify ...",
            ),
        ),
        migrations.AlterField(
            model_name="historicalstudytreatment",
            name="steroids_course_duration",
            field=models.IntegerField(
                blank=True,
                help_text="in days",
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="Length of steroid course?",
            ),
        ),
        migrations.AlterField(
            model_name="studytreatment",
            name="cm_confirmed",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                max_length=15,
                verbose_name="Cryptococcal meningitis confirmed?",
            ),
        ),
        migrations.AlterField(
            model_name="studytreatment",
            name="cm_tx_administered",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                max_length=15,
                verbose_name="Cryptococcal meningitis treatment administered?",
            ),
        ),
        migrations.AlterField(
            model_name="studytreatment",
            name="cm_tx_given_other",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other CM treatment given, please specify ...",
            ),
        ),
        migrations.AlterField(
            model_name="studytreatment",
            name="steroids_course_duration",
            field=models.IntegerField(
                blank=True,
                help_text="in days",
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="Length of steroid course?",
            ),
        ),
    ]
