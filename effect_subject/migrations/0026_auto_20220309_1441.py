# Generated by Django 3.2.8 on 2022-03-09 12:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("effect_subject", "0025_auto_20220304_1312"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalmentalstatus",
            name="ecog_score",
            field=models.CharField(
                choices=[
                    (
                        "0",
                        "[0] Fully active, able to carry on all pre-disease performance without restriction",
                    ),
                    (
                        "1",
                        "[1] Restricted in physically strenuous activity but ambulatory and able to carry out work of a light or sedentary nature, e.g., light house work, office work",
                    ),
                    (
                        "2",
                        "[2] Ambulatory and capable of all self-care but unable to carry out any work activities; up and about more than 50% of waking hours ",
                    ),
                    (
                        "3",
                        "[3] Capable of only limited self-care; confined to bed or chair more than 50% of waking hours",
                    ),
                    (
                        "4",
                        "[4] Completely disabled; cannot carry on any self-care; totally confined to bed or chair",
                    ),
                    ("5", "[5] Deceased"),
                ],
                max_length=15,
                verbose_name="ECOG score",
            ),
        ),
        migrations.AlterField(
            model_name="historicalmentalstatus",
            name="glasgow_coma_score",
            field=models.IntegerField(
                help_text="/15",
                validators=[
                    django.core.validators.MinValueValidator(3),
                    django.core.validators.MaxValueValidator(15),
                ],
                verbose_name="Glasgow Coma Score",
            ),
        ),
        migrations.AlterField(
            model_name="historicalvitalsigns",
            name="action_identifier",
            field=models.CharField(db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalvitalsigns",
            name="tracking_identifier",
            field=models.CharField(db_index=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name="mentalstatus",
            name="ecog_score",
            field=models.CharField(
                choices=[
                    (
                        "0",
                        "[0] Fully active, able to carry on all pre-disease performance without restriction",
                    ),
                    (
                        "1",
                        "[1] Restricted in physically strenuous activity but ambulatory and able to carry out work of a light or sedentary nature, e.g., light house work, office work",
                    ),
                    (
                        "2",
                        "[2] Ambulatory and capable of all self-care but unable to carry out any work activities; up and about more than 50% of waking hours ",
                    ),
                    (
                        "3",
                        "[3] Capable of only limited self-care; confined to bed or chair more than 50% of waking hours",
                    ),
                    (
                        "4",
                        "[4] Completely disabled; cannot carry on any self-care; totally confined to bed or chair",
                    ),
                    ("5", "[5] Deceased"),
                ],
                max_length=15,
                verbose_name="ECOG score",
            ),
        ),
        migrations.AlterField(
            model_name="mentalstatus",
            name="glasgow_coma_score",
            field=models.IntegerField(
                help_text="/15",
                validators=[
                    django.core.validators.MinValueValidator(3),
                    django.core.validators.MaxValueValidator(15),
                ],
                verbose_name="Glasgow Coma Score",
            ),
        ),
        migrations.AlterField(
            model_name="vitalsigns",
            name="action_identifier",
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="vitalsigns",
            name="tracking_identifier",
            field=models.CharField(max_length=30, null=True, unique=True),
        ),
    ]
