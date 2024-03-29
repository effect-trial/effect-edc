# Generated by Django 3.2.13 on 2022-07-11 10:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("effect_prn", "0006_alter_protocoldeviationviolation_violation"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="historicalendofstudy",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical End of Study",
                "verbose_name_plural": "historical End of Study",
            },
        ),
        migrations.AlterModelOptions(
            name="historicalhospitalization",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Hospitalization",
                "verbose_name_plural": "historical Hospitalization",
            },
        ),
        migrations.AlterModelOptions(
            name="historicallosstofollowup",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Loss to Follow Up",
                "verbose_name_plural": "historical Loss to Follow Up",
            },
        ),
        migrations.AlterModelOptions(
            name="historicalonschedule",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical on schedule",
                "verbose_name_plural": "historical on schedules",
            },
        ),
        migrations.AlterModelOptions(
            name="historicalprotocoldeviationviolation",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Protocol Deviation/Violation",
                "verbose_name_plural": "historical Protocol Deviations/Violations",
            },
        ),
        migrations.AlterField(
            model_name="historicalendofstudy",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="historicalhospitalization",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="historicallosstofollowup",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="historicalonschedule",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="historicalprotocoldeviationviolation",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
    ]
