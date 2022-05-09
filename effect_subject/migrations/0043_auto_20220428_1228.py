# Generated by Django 3.2.8 on 2022-04-28 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("effect_subject", "0042_auto_20220428_1146"),
    ]

    operations = [
        migrations.AlterField(
            model_name="adherence",
            name="on_arv",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Is the patient receiving ARVs?",
            ),
        ),
        migrations.AlterField(
            model_name="adherence",
            name="on_fcon",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Is the patient receiving Fluconazole?",
            ),
        ),
        migrations.AlterField(
            model_name="historicaladherence",
            name="on_arv",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Is the patient receiving ARVs?",
            ),
        ),
        migrations.AlterField(
            model_name="historicaladherence",
            name="on_fcon",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Is the patient receiving Fluconazole?",
            ),
        ),
        migrations.AlterField(
            model_name="historicaladherencestagefour",
            name="on_arv",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Is the patient receiving ARVs?",
            ),
        ),
        migrations.AlterField(
            model_name="historicaladherencestagefour",
            name="on_fcon",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Is the patient receiving Fluconazole?",
            ),
        ),
        migrations.AlterField(
            model_name="historicaladherencestageone",
            name="on_arv",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Is the patient receiving ARVs?",
            ),
        ),
        migrations.AlterField(
            model_name="historicaladherencestageone",
            name="on_fcon",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Is the patient receiving Fluconazole?",
            ),
        ),
        migrations.AlterField(
            model_name="historicaladherencestagethree",
            name="on_arv",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Is the patient receiving ARVs?",
            ),
        ),
        migrations.AlterField(
            model_name="historicaladherencestagethree",
            name="on_fcon",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Is the patient receiving Fluconazole?",
            ),
        ),
        migrations.AlterField(
            model_name="historicaladherencestagetwo",
            name="on_arv",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Is the patient receiving ARVs?",
            ),
        ),
        migrations.AlterField(
            model_name="historicaladherencestagetwo",
            name="on_fcon",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Is the patient receiving Fluconazole?",
            ),
        ),
    ]