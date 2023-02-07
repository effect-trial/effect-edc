# Generated by Django 3.2.11 on 2022-05-05 04:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("effect_subject", "0056_auto_20220505_0630"),
    ]

    operations = [
        migrations.AlterField(
            model_name="arvhistory",
            name="cd4_result",
            field=models.IntegerField(
                blank=True,
                help_text="mm<sup>3</sup>",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(9999),
                ],
                verbose_name="CD4 result",
            ),
        ),
        migrations.AlterField(
            model_name="arvhistory",
            name="viral_load_result",
            field=models.DecimalField(
                blank=True,
                decimal_places=3,
                help_text="copies/mL",
                max_digits=10,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(9999999),
                ],
                verbose_name="Viral load result",
            ),
        ),
        migrations.AlterField(
            model_name="historicalarvhistory",
            name="cd4_result",
            field=models.IntegerField(
                blank=True,
                help_text="mm<sup>3</sup>",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(9999),
                ],
                verbose_name="CD4 result",
            ),
        ),
        migrations.AlterField(
            model_name="historicalarvhistory",
            name="viral_load_result",
            field=models.DecimalField(
                blank=True,
                decimal_places=3,
                help_text="copies/mL",
                max_digits=10,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(9999999),
                ],
                verbose_name="Viral load result",
            ),
        ),
    ]
