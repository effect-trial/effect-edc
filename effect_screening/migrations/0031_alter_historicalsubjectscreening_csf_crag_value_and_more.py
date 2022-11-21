# Generated by Django 4.1.2 on 2022-11-07 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("effect_screening", "0030_alter_historicalsubjectscreening_site_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="csf_crag_value",
            field=models.CharField(
                choices=[
                    ("POS", "Positive"),
                    ("NEG", "Negative"),
                    ("PENDING", "Pending"),
                    ("not_done", "Not done"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=15,
                verbose_name="CSF CrAg result",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="csf_crag_value",
            field=models.CharField(
                choices=[
                    ("POS", "Positive"),
                    ("NEG", "Negative"),
                    ("PENDING", "Pending"),
                    ("not_done", "Not done"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=15,
                verbose_name="CSF CrAg result",
            ),
        ),
    ]
