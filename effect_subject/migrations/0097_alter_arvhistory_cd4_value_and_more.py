# Generated by Django 4.1.2 on 2022-11-07 11:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("effect_subject", "0096_auto_20221006_1121"),
    ]

    operations = [
        migrations.AlterField(
            model_name="arvhistory",
            name="cd4_value",
            field=models.IntegerField(
                help_text="cells/μL",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(105),
                ],
                verbose_name="CD4 result",
            ),
        ),
        migrations.AlterField(
            model_name="historicalarvhistory",
            name="cd4_value",
            field=models.IntegerField(
                help_text="cells/μL",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(105),
                ],
                verbose_name="CD4 result",
            ),
        ),
    ]