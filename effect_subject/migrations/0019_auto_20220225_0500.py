# Generated by Django 3.2.11 on 2022-02-25 02:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("effect_subject", "0018_auto_20220225_0423"),
    ]

    operations = [
        migrations.RenameField(
            model_name="historicallpcsf",
            old_name="csf_assay_datetime",
            new_name="csf_culture_assay_datetime",
        ),
        migrations.RenameField(
            model_name="lpcsf",
            old_name="csf_assay_datetime",
            new_name="csf_culture_assay_datetime",
        ),
        migrations.AddField(
            model_name="historicallpcsf",
            name="crag_lfa",
            field=models.CharField(
                choices=[
                    ("POS", "Positive"),
                    ("NEG", "Negative"),
                    ("not_done", "Not done"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=15,
                verbose_name="CrAg LFA",
            ),
        ),
        migrations.AddField(
            model_name="historicallpcsf",
            name="crf_crag_titre",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(999),
                ],
            ),
        ),
        migrations.AddField(
            model_name="historicallpcsf",
            name="crf_crag_titre_done",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=15,
                verbose_name="Was the CRF CrAg titre done",
            ),
        ),
        migrations.AddField(
            model_name="historicallpcsf",
            name="csf_positive",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("PENDING", "Pending"),
                    ("N/A", "Not applicable"),
                ],
                default="PENDING",
                help_text="Complete after getting the results.",
                max_length=18,
                verbose_name="CSF positive for cryptococcal meningitis?",
            ),
        ),
        migrations.AddField(
            model_name="historicallpcsf",
            name="csf_results_available",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                max_length=15,
                verbose_name="Are CSF results available?",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="historicallpcsf",
            name="sq_crag",
            field=models.CharField(
                choices=[
                    ("POS", "Positive"),
                    ("NEG", "Negative"),
                    ("not_done", "Not done"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=15,
                verbose_name="SQ CrAg",
            ),
        ),
        migrations.AddField(
            model_name="historicallpcsf",
            name="sq_crag_pos",
            field=models.CharField(
                choices=[("high", "High"), ("low", "Low"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=15,
                verbose_name="SQ CrAg",
            ),
        ),
        migrations.AddField(
            model_name="lpcsf",
            name="crag_lfa",
            field=models.CharField(
                choices=[
                    ("POS", "Positive"),
                    ("NEG", "Negative"),
                    ("not_done", "Not done"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=15,
                verbose_name="CrAg LFA",
            ),
        ),
        migrations.AddField(
            model_name="lpcsf",
            name="crf_crag_titre",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(999),
                ],
            ),
        ),
        migrations.AddField(
            model_name="lpcsf",
            name="crf_crag_titre_done",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=15,
                verbose_name="Was the CRF CrAg titre done",
            ),
        ),
        migrations.AddField(
            model_name="lpcsf",
            name="csf_positive",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("PENDING", "Pending"),
                    ("N/A", "Not applicable"),
                ],
                default="PENDING",
                help_text="Complete after getting the results.",
                max_length=18,
                verbose_name="CSF positive for cryptococcal meningitis?",
            ),
        ),
        migrations.AddField(
            model_name="lpcsf",
            name="csf_results_available",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                max_length=15,
                verbose_name="Are CSF results available?",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="lpcsf",
            name="sq_crag",
            field=models.CharField(
                choices=[
                    ("POS", "Positive"),
                    ("NEG", "Negative"),
                    ("not_done", "Not done"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=15,
                verbose_name="SQ CrAg",
            ),
        ),
        migrations.AddField(
            model_name="lpcsf",
            name="sq_crag_pos",
            field=models.CharField(
                choices=[("high", "High"), ("low", "Low"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=15,
                verbose_name="SQ CrAg",
            ),
        ),
        migrations.AlterField(
            model_name="historicallpcsf",
            name="india_ink",
            field=models.CharField(
                choices=[
                    ("POS", "Positive"),
                    ("NEG", "Negative"),
                    ("not_done", "Not done"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=15,
            ),
        ),
        migrations.AlterField(
            model_name="lpcsf",
            name="india_ink",
            field=models.CharField(
                choices=[
                    ("POS", "Positive"),
                    ("NEG", "Negative"),
                    ("not_done", "Not done"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=15,
            ),
        ),
    ]
