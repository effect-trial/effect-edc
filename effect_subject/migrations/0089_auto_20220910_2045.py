# Generated by Django 3.2 on 2022-09-10 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("effect_subject", "0088_auto_20220826_1549"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bloodresultschem",
            name="tracking_identifier",
        ),
        migrations.RemoveField(
            model_name="bloodresultsfbc",
            name="tracking_identifier",
        ),
        migrations.RemoveField(
            model_name="historicalbloodresultschem",
            name="tracking_identifier",
        ),
        migrations.RemoveField(
            model_name="historicalbloodresultsfbc",
            name="tracking_identifier",
        ),
        migrations.RemoveField(
            model_name="historicalsignsandsymptoms",
            name="tracking_identifier",
        ),
        migrations.RemoveField(
            model_name="historicalurinalysis",
            name="tracking_identifier",
        ),
        migrations.RemoveField(
            model_name="historicalvitalsigns",
            name="tracking_identifier",
        ),
        migrations.RemoveField(
            model_name="signsandsymptoms",
            name="tracking_identifier",
        ),
        migrations.RemoveField(
            model_name="urinalysis",
            name="tracking_identifier",
        ),
        migrations.RemoveField(
            model_name="vitalsigns",
            name="tracking_identifier",
        ),
        migrations.AlterField(
            model_name="bloodresultschem",
            name="action_identifier",
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="bloodresultsfbc",
            name="action_identifier",
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultschem",
            name="action_identifier",
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultsfbc",
            name="action_identifier",
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalsignsandsymptoms",
            name="action_identifier",
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalurinalysis",
            name="action_identifier",
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="historicalvitalsigns",
            name="action_identifier",
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="signsandsymptoms",
            name="action_identifier",
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="urinalysis",
            name="action_identifier",
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="vitalsigns",
            name="action_identifier",
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
