# Generated by Django 4.2.6 on 2023-11-01 12:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("effect_ae", "0016_alter_aefollowup_options_alter_aeinitial_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="deathreport",
            name="blurred_vision",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("unknown", "Unknown"),
                    ("N/A", "Not applicable"),
                ],
                max_length=25,
                null=True,
                verbose_name="If YES, did they complain of blurred vision?",
            ),
        ),
        migrations.AddField(
            model_name="historicaldeathreport",
            name="blurred_vision",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("unknown", "Unknown"),
                    ("N/A", "Not applicable"),
                ],
                max_length=25,
                null=True,
                verbose_name="If YES, did they complain of blurred vision?",
            ),
        ),
    ]