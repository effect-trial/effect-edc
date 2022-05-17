# Generated by Django 3.2.11 on 2022-05-11 11:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('effect_subject', '0062_auto_20220511_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloodresultsfbc',
            name='lymphocyte_diff_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(9999)], verbose_name='Lymphocyte (diff)'),
        ),
        migrations.AlterField(
            model_name='bloodresultsfbc',
            name='lymphocyte_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(9999)], verbose_name='Lymphocyte (abs)'),
        ),
        migrations.AlterField(
            model_name='bloodresultsfbc',
            name='neutrophil_diff_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(9999)], verbose_name='Neutrophil (diff)'),
        ),
        migrations.AlterField(
            model_name='bloodresultsfbc',
            name='neutrophil_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(9999)], verbose_name='Neutrophil (abs)'),
        ),
        migrations.AlterField(
            model_name='historicalbloodresultsfbc',
            name='lymphocyte_diff_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(9999)], verbose_name='Lymphocyte (diff)'),
        ),
        migrations.AlterField(
            model_name='historicalbloodresultsfbc',
            name='lymphocyte_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(9999)], verbose_name='Lymphocyte (abs)'),
        ),
        migrations.AlterField(
            model_name='historicalbloodresultsfbc',
            name='neutrophil_diff_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(9999)], verbose_name='Neutrophil (diff)'),
        ),
        migrations.AlterField(
            model_name='historicalbloodresultsfbc',
            name='neutrophil_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(9999)], verbose_name='Neutrophil (abs)'),
        ),
    ]