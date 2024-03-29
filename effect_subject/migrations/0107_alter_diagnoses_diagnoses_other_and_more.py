# Generated by Django 4.1.7 on 2023-08-09 15:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("effect_subject", "0106_alter_historicalmentalstatus_modified_rankin_score_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="diagnoses",
            name="diagnoses_other",
            field=models.TextField(
                blank=True,
                max_length=150,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldiagnoses",
            name="diagnoses_other",
            field=models.TextField(
                blank=True,
                max_length=150,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
    ]
