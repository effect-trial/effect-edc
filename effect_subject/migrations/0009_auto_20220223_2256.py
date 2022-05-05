# Generated by Django 3.2.11 on 2022-02-23 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("effect_subject", "0008_auto_20220223_2236"),
    ]

    operations = [
        migrations.RenameField(
            model_name="histopathology",
            old_name="tissue_biopsy_taken",
            new_name="tissue_biopsy_performed",
        ),
        migrations.RenameField(
            model_name="historicalhistopathology",
            old_name="tissue_biopsy_taken",
            new_name="tissue_biopsy_performed",
        ),
        migrations.AlterField(
            model_name="bloodculture",
            name="blood_culture_result",
            field=models.CharField(
                choices=[
                    ("POS", "Positive"),
                    ("no_growth", "No growth"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=10,
                verbose_name="Blood culture result",
            ),
        ),
        migrations.AlterField(
            model_name="histopathology",
            name="tissue_biopsy_result",
            field=models.CharField(
                choices=[
                    ("POS", "Positive"),
                    ("no_growth", "No growth"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=10,
                verbose_name="Tissue biopsy results",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbloodculture",
            name="blood_culture_result",
            field=models.CharField(
                choices=[
                    ("POS", "Positive"),
                    ("no_growth", "No growth"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=10,
                verbose_name="Blood culture result",
            ),
        ),
        migrations.AlterField(
            model_name="historicalhistopathology",
            name="tissue_biopsy_result",
            field=models.CharField(
                choices=[
                    ("POS", "Positive"),
                    ("no_growth", "No growth"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=10,
                verbose_name="Tissue biopsy results",
            ),
        ),
    ]
