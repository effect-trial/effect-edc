# Generated by Django 3.2.11 on 2022-05-05 03:30

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("effect_subject", "0055_auto_20220505_0623"),
    ]

    operations = [
        migrations.RenameField(
            model_name="arvhistory",
            old_name="has_cd4",
            new_name="has_cd4_result",
        ),
        migrations.RenameField(
            model_name="historicalarvhistory",
            old_name="has_cd4",
            new_name="has_cd4_result",
        ),
    ]
