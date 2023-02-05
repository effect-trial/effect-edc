# Generated by Django 3.2.13 on 2022-06-15 15:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("effect_subject", "0074_auto_20220615_1656"),
    ]

    operations = [
        migrations.AlterField(
            model_name="arvhistory",
            name="cd4_value",
            field=models.IntegerField(
                help_text="mm<sup>3</sup>",
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
                help_text="mm<sup>3</sup>",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(105),
                ],
                verbose_name="CD4 result",
            ),
        ),
    ]
