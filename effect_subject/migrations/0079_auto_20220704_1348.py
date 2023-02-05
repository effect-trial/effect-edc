# Generated by Django 3.2.13 on 2022-07-04 11:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("effect_subject", "0078_auto_20220624_1927"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalmentalstatus",
            name="any_other_problems",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="Answer only at scheduled Week 10 and Month 6 visits",
                max_length=15,
                verbose_name="Has the illness left the participant with any other problems?",
            ),
        ),
        migrations.AddField(
            model_name="historicalmentalstatus",
            name="require_help",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="Answer only at scheduled Week 10 and Month 6 visits",
                max_length=15,
                verbose_name="Does the participant require help from anybody for everyday activities?",
            ),
        ),
        migrations.AddField(
            model_name="mentalstatus",
            name="any_other_problems",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="Answer only at scheduled Week 10 and Month 6 visits",
                max_length=15,
                verbose_name="Has the illness left the participant with any other problems?",
            ),
        ),
        migrations.AddField(
            model_name="mentalstatus",
            name="require_help",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="Answer only at scheduled Week 10 and Month 6 visits",
                max_length=15,
                verbose_name="Does the participant require help from anybody for everyday activities?",
            ),
        ),
    ]
