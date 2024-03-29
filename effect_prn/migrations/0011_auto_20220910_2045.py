# Generated by Django 3.2 on 2022-09-10 18:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("effect_prn", "0010_auto_20220824_1919"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="endofstudy",
            name="tracking_identifier",
        ),
        migrations.RemoveField(
            model_name="historicalendofstudy",
            name="tracking_identifier",
        ),
        migrations.RemoveField(
            model_name="historicalhospitalization",
            name="tracking_identifier",
        ),
        migrations.RemoveField(
            model_name="historicallosstofollowup",
            name="tracking_identifier",
        ),
        migrations.RemoveField(
            model_name="historicalprotocoldeviationviolation",
            name="tracking_identifier",
        ),
        migrations.RemoveField(
            model_name="hospitalization",
            name="tracking_identifier",
        ),
        migrations.RemoveField(
            model_name="losstofollowup",
            name="tracking_identifier",
        ),
        migrations.RemoveField(
            model_name="protocoldeviationviolation",
            name="tracking_identifier",
        ),
        migrations.AlterField(
            model_name="endofstudy",
            name="action_identifier",
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="historicalendofstudy",
            name="action_identifier",
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalhospitalization",
            name="action_identifier",
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicallosstofollowup",
            name="action_identifier",
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalprotocoldeviationviolation",
            name="action_identifier",
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="hospitalization",
            name="action_identifier",
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="losstofollowup",
            name="action_identifier",
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="protocoldeviationviolation",
            name="action_identifier",
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
