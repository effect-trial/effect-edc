# Generated by Django 3.2.11 on 2022-05-05 04:18

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("effect_prn", "0002_auto_20220430_1945"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="historicallosstofollowup",
            options={
                "get_latest_by": "history_date",
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Loss to Follow Up",
            },
        ),
        migrations.AlterModelOptions(
            name="losstofollowup",
            options={
                "verbose_name": "Loss to Follow Up",
                "verbose_name_plural": "Loss to Follow Up",
            },
        ),
    ]
