# Generated by Django 3.2 on 2022-09-10 18:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("effect_consent", "0004_auto_20220824_1919"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicalsubjectreconsent",
            name="tracking_identifier",
        ),
        migrations.RemoveField(
            model_name="subjectreconsent",
            name="tracking_identifier",
        ),
        migrations.AlterField(
            model_name="historicalsubjectreconsent",
            name="action_identifier",
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="subjectreconsent",
            name="action_identifier",
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
