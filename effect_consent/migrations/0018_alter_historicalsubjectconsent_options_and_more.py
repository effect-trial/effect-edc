# Generated by Django 4.2.6 on 2024-03-01 10:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("effect_consent", "0017_delete_subjectconsentupdatev2_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="historicalsubjectconsent",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Consent",
                "verbose_name_plural": "historical Consents",
            },
        ),
        migrations.AlterModelOptions(
            name="subjectconsent",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "verbose_name": "Consent",
                "verbose_name_plural": "Consents",
            },
        ),
    ]
