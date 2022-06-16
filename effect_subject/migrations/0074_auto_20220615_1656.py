# Generated by Django 3.2.13 on 2022-06-15 14:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('effect_subject', '0073_auto_20220615_1311'),
    ]

    operations = [
        migrations.RenameField(
            model_name='arvhistory',
            old_name='cd4_result',
            new_name='cd4_value',
        ),
        migrations.RemoveField(
            model_name='arvhistory',
            name='has_cd4_result',
        ),
        migrations.RenameField(
            model_name='historicalarvhistory',
            old_name='cd4_result',
            new_name='cd4_value',
        ),
        migrations.RemoveField(
            model_name='historicalarvhistory',
            name='has_cd4_result',
        ),
    ]