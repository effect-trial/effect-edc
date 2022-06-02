# Generated by Django 3.2.7 on 2021-11-09 01:18

import uuid

import _socket
import django.contrib.sites.managers
import django.db.models.deletion
import django_audit_fields.fields.hostname_modification_field
import django_audit_fields.fields.userfield
import django_audit_fields.fields.uuid_auto_field
import django_audit_fields.models.audit_model_mixin
import django_revision.revision_field
import edc_model.models.fields.other_charfield
import edc_model.validators.date
import edc_protocol.validators
import edc_utils.date
import edc_visit_tracking.managers
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("sites", "0002_alter_domain_unique"),
        ("effect_subject", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Followup",
            fields=[
                (
                    "revision",
                    django_revision.revision_field.RevisionField(
                        blank=True,
                        editable=False,
                        help_text="System field. Git repository tag:branch:commit.",
                        max_length=75,
                        null=True,
                        verbose_name="Revision",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow
                    ),
                ),
                (
                    "user_created",
                    django_audit_fields.fields.userfield.UserField(
                        blank=True,
                        help_text="Updated by admin.save_model",
                        max_length=50,
                        verbose_name="user created",
                    ),
                ),
                (
                    "user_modified",
                    django_audit_fields.fields.userfield.UserField(
                        blank=True,
                        help_text="Updated by admin.save_model",
                        max_length=50,
                        verbose_name="user modified",
                    ),
                ),
                (
                    "hostname_created",
                    models.CharField(
                        blank=True,
                        default=_socket.gethostname,
                        help_text="System field. (modified on create only)",
                        max_length=60,
                    ),
                ),
                (
                    "hostname_modified",
                    django_audit_fields.fields.hostname_modification_field.HostnameModificationField(
                        blank=True,
                        help_text="System field. (modified on every save)",
                        max_length=50,
                    ),
                ),
                ("device_created", models.CharField(blank=True, max_length=10)),
                ("device_modified", models.CharField(blank=True, max_length=10)),
                (
                    "id",
                    django_audit_fields.fields.uuid_auto_field.UUIDAutoField(
                        blank=True,
                        editable=False,
                        help_text="System auto field. UUID primary key.",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "report_datetime",
                    models.DateTimeField(
                        default=edc_utils.date.get_utcnow,
                        help_text="If reporting today, use today's date/time, otherwise use the date/time this information was reported.",
                        validators=[
                            edc_protocol.validators.datetime_not_before_study_start,
                            edc_model.validators.date.datetime_not_future,
                        ],
                        verbose_name="Report Date",
                    ),
                ),
                ("consent_model", models.CharField(editable=False, max_length=50, null=True)),
                (
                    "consent_version",
                    models.CharField(editable=False, max_length=10, null=True),
                ),
                (
                    "crf_status",
                    models.CharField(
                        choices=[
                            ("INCOMPLETE", "Incomplete (some data pending)"),
                            ("COMPLETE", "Complete"),
                        ],
                        default="COMPLETE",
                        help_text="If some data is still pending, flag this CRF as incomplete",
                        max_length=25,
                        verbose_name="CRF status",
                    ),
                ),
                (
                    "crf_status_comments",
                    models.TextField(
                        blank=True,
                        help_text="for example, why some data is still pending",
                        null=True,
                        verbose_name="Any comments related to status of this CRF",
                    ),
                ),
                (
                    "assessment_type",
                    models.CharField(
                        choices=[("telephone", "Telephone"), ("in_person", "In person")],
                        max_length=15,
                        verbose_name="Was this a telephone follow up or an in person visit?",
                    ),
                ),
                (
                    "info_source",
                    models.CharField(
                        choices=[
                            ("patient", "Patient"),
                            ("next_of_kin", "Next of kin"),
                            ("OTHER", "Other"),
                        ],
                        default="patient",
                        max_length=15,
                        verbose_name="If by telephone, who did you speak to?",
                    ),
                ),
                (
                    "info_source_other",
                    edc_model.models.fields.other_charfield.OtherCharField(
                        blank=True,
                        max_length=35,
                        null=True,
                        verbose_name="If other, please specify ...",
                    ),
                ),
                (
                    "survival_status",
                    models.CharField(
                        choices=[
                            ("alive_well", "Alive and well"),
                            ("alive_unwell", "Alive, but unwell"),
                            ("dead", "Deceased"),
                        ],
                        max_length=15,
                        verbose_name="What is the patient status?",
                    ),
                ),
                (
                    "hospitalized",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")],
                        max_length=15,
                        verbose_name="Has the patient been hospitalized since the last assessment?",
                    ),
                ),
                (
                    "adherence_counselling",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")],
                        max_length=15,
                        verbose_name="Was adherence counselling given?",
                    ),
                ),
                (
                    "site",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="sites.site",
                    ),
                ),
                (
                    "subject_visit",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="effect_subject.subjectvisit",
                    ),
                ),
            ],
            options={
                "verbose_name": "Clinical Assessment",
                "verbose_name_plural": "Clinical Assessment",
                "ordering": ("-modified", "-created"),
                "get_latest_by": "modified",
                "abstract": False,
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
            },
            managers=[
                ("on_site", django.contrib.sites.managers.CurrentSiteManager()),
                ("objects", edc_visit_tracking.managers.CrfModelManager()),
            ],
        ),
        migrations.CreateModel(
            name="HistoricalFollowup",
            fields=[
                (
                    "revision",
                    django_revision.revision_field.RevisionField(
                        blank=True,
                        editable=False,
                        help_text="System field. Git repository tag:branch:commit.",
                        max_length=75,
                        null=True,
                        verbose_name="Revision",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow
                    ),
                ),
                (
                    "user_created",
                    django_audit_fields.fields.userfield.UserField(
                        blank=True,
                        help_text="Updated by admin.save_model",
                        max_length=50,
                        verbose_name="user created",
                    ),
                ),
                (
                    "user_modified",
                    django_audit_fields.fields.userfield.UserField(
                        blank=True,
                        help_text="Updated by admin.save_model",
                        max_length=50,
                        verbose_name="user modified",
                    ),
                ),
                (
                    "hostname_created",
                    models.CharField(
                        blank=True,
                        default=_socket.gethostname,
                        help_text="System field. (modified on create only)",
                        max_length=60,
                    ),
                ),
                (
                    "hostname_modified",
                    django_audit_fields.fields.hostname_modification_field.HostnameModificationField(
                        blank=True,
                        help_text="System field. (modified on every save)",
                        max_length=50,
                    ),
                ),
                ("device_created", models.CharField(blank=True, max_length=10)),
                ("device_modified", models.CharField(blank=True, max_length=10)),
                (
                    "id",
                    django_audit_fields.fields.uuid_auto_field.UUIDAutoField(
                        blank=True,
                        db_index=True,
                        editable=False,
                        help_text="System auto field. UUID primary key.",
                    ),
                ),
                (
                    "report_datetime",
                    models.DateTimeField(
                        default=edc_utils.date.get_utcnow,
                        help_text="If reporting today, use today's date/time, otherwise use the date/time this information was reported.",
                        validators=[
                            edc_protocol.validators.datetime_not_before_study_start,
                            edc_model.validators.date.datetime_not_future,
                        ],
                        verbose_name="Report Date",
                    ),
                ),
                ("consent_model", models.CharField(editable=False, max_length=50, null=True)),
                (
                    "consent_version",
                    models.CharField(editable=False, max_length=10, null=True),
                ),
                (
                    "history_id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "crf_status",
                    models.CharField(
                        choices=[
                            ("INCOMPLETE", "Incomplete (some data pending)"),
                            ("COMPLETE", "Complete"),
                        ],
                        default="COMPLETE",
                        help_text="If some data is still pending, flag this CRF as incomplete",
                        max_length=25,
                        verbose_name="CRF status",
                    ),
                ),
                (
                    "crf_status_comments",
                    models.TextField(
                        blank=True,
                        help_text="for example, why some data is still pending",
                        null=True,
                        verbose_name="Any comments related to status of this CRF",
                    ),
                ),
                (
                    "assessment_type",
                    models.CharField(
                        choices=[("telephone", "Telephone"), ("in_person", "In person")],
                        max_length=15,
                        verbose_name="Was this a telephone follow up or an in person visit?",
                    ),
                ),
                (
                    "info_source",
                    models.CharField(
                        choices=[
                            ("patient", "Patient"),
                            ("next_of_kin", "Next of kin"),
                            ("OTHER", "Other"),
                        ],
                        default="patient",
                        max_length=15,
                        verbose_name="If by telephone, who did you speak to?",
                    ),
                ),
                (
                    "info_source_other",
                    edc_model.models.fields.other_charfield.OtherCharField(
                        blank=True,
                        max_length=35,
                        null=True,
                        verbose_name="If other, please specify ...",
                    ),
                ),
                (
                    "survival_status",
                    models.CharField(
                        choices=[
                            ("alive_well", "Alive and well"),
                            ("alive_unwell", "Alive, but unwell"),
                            ("dead", "Deceased"),
                        ],
                        max_length=15,
                        verbose_name="What is the patient status?",
                    ),
                ),
                (
                    "hospitalized",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")],
                        max_length=15,
                        verbose_name="Has the patient been hospitalized since the last assessment?",
                    ),
                ),
                (
                    "adherence_counselling",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")],
                        max_length=15,
                        verbose_name="Was adherence counselling given?",
                    ),
                ),
                ("history_date", models.DateTimeField()),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "site",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="sites.site",
                    ),
                ),
                (
                    "subject_visit",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="effect_subject.subjectvisit",
                    ),
                ),
            ],
            options={
                "verbose_name": "historical Clinical Assessment",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": "history_date",
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.RemoveField(
            model_name="historicalclinicalassessment",
            name="history_user",
        ),
        migrations.RemoveField(
            model_name="historicalclinicalassessment",
            name="site",
        ),
        migrations.RemoveField(
            model_name="historicalclinicalassessment",
            name="subject_visit",
        ),
        migrations.DeleteModel(
            name="ClinicalAssessment",
        ),
        migrations.DeleteModel(
            name="HistoricalClinicalAssessment",
        ),
        migrations.AddIndex(
            model_name="followup",
            index=models.Index(
                fields=["subject_visit", "site", "id"], name="effect_subj_subject_64f16e_idx"
            ),
        ),
    ]
