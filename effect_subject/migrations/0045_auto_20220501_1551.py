# Generated by Django 3.2.11 on 2022-05-01 12:51

import uuid

import _socket
import django.contrib.sites.managers
import django.db.models.deletion
import django_audit_fields.fields.hostname_modification_field
import django_audit_fields.fields.userfield
import django_audit_fields.fields.uuid_auto_field
import django_audit_fields.models.audit_model_mixin
import django_revision.revision_field
import edc_model.validators.date
import edc_protocol.validators
import edc_utils.date
import edc_visit_tracking.managers
import simple_history.models
from django.conf import settings
from django.db import migrations, models

import effect_subject.models.subject_visit


class Migration(migrations.Migration):
    dependencies = [
        ("sites", "0002_alter_domain_unique"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("effect_lists", "0008_delete_medicinesday14"),
        ("effect_subject", "0044_auto_20220430_1945"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="chestxray",
            options={
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Chest X-ray",
                "verbose_name_plural": "Chest X-rays",
            },
        ),
        migrations.AlterField(
            model_name="chestxray",
            name="chest_xray",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Was a chest x-ray performed?",
            ),
        ),
        migrations.AlterField(
            model_name="chestxray",
            name="chest_xray_date",
            field=models.DateField(
                blank=True, null=True, verbose_name="If YES, date performed?"
            ),
        ),
        migrations.AlterField(
            model_name="chestxray",
            name="chest_xray_results",
            field=models.ManyToManyField(
                blank=True,
                to="effect_lists.XRayResults",
                verbose_name="If YES, indicate results?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalchestxray",
            name="chest_xray",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Was a chest x-ray performed?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalchestxray",
            name="chest_xray_date",
            field=models.DateField(
                blank=True, null=True, verbose_name="If YES, date performed?"
            ),
        ),
    ]
