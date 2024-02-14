# Generated by Django 4.2.5 on 2023-10-02 19:14

import _socket
import django.contrib.sites.managers
from django.db import migrations, models
import django.db.models.manager
import django_audit_fields.fields.hostname_modification_field


class Migration(migrations.Migration):
    dependencies = [
        ("effect_consent", "0007_alter_historicalsubjectconsent_language_and_more"),
    ]

    operations = [
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
                "get_latest_by": "consent_datetime",
                "ordering": ("created",),
                "verbose_name": "Subject Consent",
                "verbose_name_plural": "Subject Consents",
            },
        ),
        migrations.AlterModelManagers(
            name="subjectconsent",
            managers=[
                ("on_site", django.contrib.sites.managers.CurrentSiteManager()),
                ("objects", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name="historicalsubjectconsent",
            name="device_created",
            field=models.CharField(blank=True, max_length=10, verbose_name="Device created"),
        ),
        migrations.AlterField(
            model_name="historicalsubjectconsent",
            name="device_modified",
            field=models.CharField(blank=True, max_length=10, verbose_name="Device modified"),
        ),
        migrations.AlterField(
            model_name="historicalsubjectconsent",
            name="hostname_created",
            field=models.CharField(
                blank=True,
                default=_socket.gethostname,
                help_text="System field. (modified on create only)",
                max_length=60,
                verbose_name="Hostname created",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectconsent",
            name="hostname_modified",
            field=django_audit_fields.fields.hostname_modification_field.HostnameModificationField(
                blank=True,
                help_text="System field. (modified on every save)",
                max_length=50,
                verbose_name="Hostname modified",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectconsent",
            name="language",
            field=models.CharField(
                choices=[
                    ("en-gb", "British English"),
                    ("en", "English"),
                    ("af", "Afrikaans"),
                    ("mas", "Maasai"),
                    ("st", "Sotho, Southern"),
                    ("sw", "Swahili"),
                    ("tn", "Tswana"),
                    ("vi", "Vietnamese"),
                    ("xh", "Xhosa"),
                    ("zu", "Zulu"),
                ],
                help_text="The language used for the consent process will also be used during data collection.",
                max_length=25,
                verbose_name="Language of consent",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectreconsent",
            name="device_created",
            field=models.CharField(blank=True, max_length=10, verbose_name="Device created"),
        ),
        migrations.AlterField(
            model_name="historicalsubjectreconsent",
            name="device_modified",
            field=models.CharField(blank=True, max_length=10, verbose_name="Device modified"),
        ),
        migrations.AlterField(
            model_name="historicalsubjectreconsent",
            name="hostname_created",
            field=models.CharField(
                blank=True,
                default=_socket.gethostname,
                help_text="System field. (modified on create only)",
                max_length=60,
                verbose_name="Hostname created",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectreconsent",
            name="hostname_modified",
            field=django_audit_fields.fields.hostname_modification_field.HostnameModificationField(
                blank=True,
                help_text="System field. (modified on every save)",
                max_length=50,
                verbose_name="Hostname modified",
            ),
        ),
        migrations.AlterField(
            model_name="subjectconsent",
            name="device_created",
            field=models.CharField(blank=True, max_length=10, verbose_name="Device created"),
        ),
        migrations.AlterField(
            model_name="subjectconsent",
            name="device_modified",
            field=models.CharField(blank=True, max_length=10, verbose_name="Device modified"),
        ),
        migrations.AlterField(
            model_name="subjectconsent",
            name="hostname_created",
            field=models.CharField(
                blank=True,
                default=_socket.gethostname,
                help_text="System field. (modified on create only)",
                max_length=60,
                verbose_name="Hostname created",
            ),
        ),
        migrations.AlterField(
            model_name="subjectconsent",
            name="hostname_modified",
            field=django_audit_fields.fields.hostname_modification_field.HostnameModificationField(
                blank=True,
                help_text="System field. (modified on every save)",
                max_length=50,
                verbose_name="Hostname modified",
            ),
        ),
        migrations.AlterField(
            model_name="subjectconsent",
            name="language",
            field=models.CharField(
                choices=[
                    ("en-gb", "British English"),
                    ("en", "English"),
                    ("af", "Afrikaans"),
                    ("mas", "Maasai"),
                    ("st", "Sotho, Southern"),
                    ("sw", "Swahili"),
                    ("tn", "Tswana"),
                    ("vi", "Vietnamese"),
                    ("xh", "Xhosa"),
                    ("zu", "Zulu"),
                ],
                help_text="The language used for the consent process will also be used during data collection.",
                max_length=25,
                verbose_name="Language of consent",
            ),
        ),
        migrations.AlterField(
            model_name="subjectreconsent",
            name="device_created",
            field=models.CharField(blank=True, max_length=10, verbose_name="Device created"),
        ),
        migrations.AlterField(
            model_name="subjectreconsent",
            name="device_modified",
            field=models.CharField(blank=True, max_length=10, verbose_name="Device modified"),
        ),
        migrations.AlterField(
            model_name="subjectreconsent",
            name="hostname_created",
            field=models.CharField(
                blank=True,
                default=_socket.gethostname,
                help_text="System field. (modified on create only)",
                max_length=60,
                verbose_name="Hostname created",
            ),
        ),
        migrations.AlterField(
            model_name="subjectreconsent",
            name="hostname_modified",
            field=django_audit_fields.fields.hostname_modification_field.HostnameModificationField(
                blank=True,
                help_text="System field. (modified on every save)",
                max_length=50,
                verbose_name="Hostname modified",
            ),
        ),
    ]