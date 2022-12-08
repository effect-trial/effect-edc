# Generated by Django 4.1.2 on 2022-11-15 16:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("effect_subject", "0097_alter_arvhistory_cd4_value_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="arvhistory",
            name="art_doses_missed",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(31),
                ],
                verbose_name="If not `adherent`, how many doses missed in the last month?",
            ),
        ),
        migrations.AlterField(
            model_name="arvhistory",
            name="is_adherent",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("defaulted", "Defaulted"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=10,
                verbose_name="If the participant is currently on ART, are they <u>adherent</u> to their <u>current</u> ART regimen?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalarvhistory",
            name="art_doses_missed",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(31),
                ],
                verbose_name="If not `adherent`, how many doses missed in the last month?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalarvhistory",
            name="is_adherent",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("defaulted", "Defaulted"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=10,
                verbose_name="If the participant is currently on ART, are they <u>adherent</u> to their <u>current</u> ART regimen?",
            ),
        ),
    ]