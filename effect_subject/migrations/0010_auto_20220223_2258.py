# Generated by Django 3.2.11 on 2022-02-23 19:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("effect_subject", "0009_auto_20220223_2256"),
    ]

    operations = [
        migrations.RenameField(
            model_name="histopathology",
            old_name="tissue_biopsy_day_taken",
            new_name="tissue_biopsy_day",
        ),
        migrations.RenameField(
            model_name="historicalhistopathology",
            old_name="tissue_biopsy_day_taken",
            new_name="tissue_biopsy_day",
        ),
    ]
