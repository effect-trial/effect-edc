# Generated by Django 4.2.5 on 2023-10-02 19:14

import _socket
import django_audit_fields.fields.hostname_modification_field
import edc_screening.model_mixins.screening_model_mixin
import edc_sites.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "effect_screening",
            "0033_alter_historicalsubjectscreening_eligibility_datetime_and_more",
        ),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="subjectscreening",
            managers=[
                (
                    "objects",
                    edc_screening.model_mixins.screening_model_mixin.ScreeningManager(),
                ),
                ("on_site", edc_sites.models.CurrentSiteManager()),
            ],
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="device_created",
            field=models.CharField(blank=True, max_length=10, verbose_name="Device created"),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="device_modified",
            field=models.CharField(blank=True, max_length=10, verbose_name="Device modified"),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
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
            model_name="historicalsubjectscreening",
            name="hostname_modified",
            field=django_audit_fields.fields.hostname_modification_field.HostnameModificationField(
                blank=True,
                help_text="System field. (modified on every save)",
                max_length=50,
                verbose_name="Hostname modified",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="device_created",
            field=models.CharField(blank=True, max_length=10, verbose_name="Device created"),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="device_modified",
            field=models.CharField(blank=True, max_length=10, verbose_name="Device modified"),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
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
            model_name="subjectscreening",
            name="hostname_modified",
            field=django_audit_fields.fields.hostname_modification_field.HostnameModificationField(
                blank=True,
                help_text="System field. (modified on every save)",
                max_length=50,
                verbose_name="Hostname modified",
            ),
        ),
    ]