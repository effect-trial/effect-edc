# Generated by Django 4.2.11 on 2024-08-14 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("effect_reports", "0003_historicalconfirmedserumcragdate_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="consentedserumcragdate",
            options={
                "default_permissions": ("view", "export", "viewallsites"),
                "verbose_name": "Redmine #488.1 Consented Serum Crag Date",
                "verbose_name_plural": "Redmine #488.1 Consented Serum Crag Dates",
            },
        ),
    ]
