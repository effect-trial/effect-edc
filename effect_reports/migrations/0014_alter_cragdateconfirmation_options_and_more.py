# Generated by Django 4.2.11 on 2024-07-31 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("effect_reports", "0013_historicalcragdateconfirmation_cragdateconfirmation"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="cragdateconfirmation",
            options={
                "default_permissions": ("view", "export", "viewallsites"),
                "verbose_name": "Screening Crag Date Confirmation 2",
                "verbose_name_plural": "Screening Crag Date Confirmations 2",
            },
        ),
        migrations.AddField(
            model_name="cragdateconfirmation",
            name="eligiblility_date",
            field=models.DateField(null=True),
        ),
        migrations.DeleteModel(
            name="HistoricalCragDateConfirmation",
        ),
    ]
