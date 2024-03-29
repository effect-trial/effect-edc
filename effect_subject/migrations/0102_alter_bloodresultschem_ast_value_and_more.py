# Generated by Django 4.1.7 on 2023-05-15 16:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("effect_subject", "0101_alter_bloodresultschem_ast_value_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bloodresultschem",
            name="ast_value",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=8,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(9999),
                ],
                verbose_name="AST",
            ),
        ),
        migrations.AlterField(
            model_name="bloodresultschem",
            name="ggt_value",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=8,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(9999),
                ],
                verbose_name="GGT",
            ),
        ),
        migrations.AlterField(
            model_name="bloodresultsfbc",
            name="platelets_value",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=8,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(9999),
                ],
                verbose_name="Platelets",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultschem",
            name="ast_value",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=8,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(9999),
                ],
                verbose_name="AST",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultschem",
            name="ggt_value",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=8,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(9999),
                ],
                verbose_name="GGT",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultsfbc",
            name="platelets_value",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=8,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(9999),
                ],
                verbose_name="Platelets",
            ),
        ),
    ]
