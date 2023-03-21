# Generated by Django 4.1.7 on 2023-03-21 16:14

import _socket
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django_audit_fields.fields.hostname_modification_field
import django_audit_fields.fields.userfield
import django_audit_fields.fields.uuid_auto_field
import django_audit_fields.models.audit_model_mixin
import django_revision.revision_field
import edc_model_fields.fields.other_charfield
import edc_sites.model_mixins
import simple_history.models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("sites", "0002_alter_domain_unique"),
        ("effect_subject", "0101_alter_bloodresultschem_results_abnormal_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="HistoricalFlucytMissedDoses",
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
                    "day_missed",
                    models.IntegerField(
                        choices=[
                            (1, "Day 1"),
                            (2, "Day 2"),
                            (3, "Day 3"),
                            (4, "Day 4"),
                            (5, "Day 5"),
                            (6, "Day 6"),
                            (7, "Day 7"),
                            (8, "Day 8"),
                            (9, "Day 9"),
                            (10, "Day 10"),
                            (11, "Day 11"),
                            (12, "Day 12"),
                            (13, "Day 13"),
                            (14, "Day 14"),
                            (15, "Day 15"),
                        ],
                        verbose_name="Day missed:",
                    ),
                ),
                (
                    "missed_reason",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("toxicity", "Toxicity"),
                            ("missed", "Missed"),
                            ("REFUSED", "Refused"),
                            ("not_required", "Not required according to protocol"),
                            ("OTHER", "Other"),
                        ],
                        max_length=25,
                        verbose_name="Reason:",
                    ),
                ),
                (
                    "missed_reason_other",
                    edc_model_fields.fields.other_charfield.OtherCharField(
                        blank=True,
                        max_length=35,
                        null=True,
                        verbose_name="If other, please specify ...",
                    ),
                ),
                (
                    "doses_missed",
                    models.IntegerField(
                        choices=[
                            (1, "1 Dose"),
                            (2, "2 Doses"),
                            (3, "3 Doses"),
                            (4, "4 Doses"),
                        ],
                        verbose_name="Doses missed:",
                    ),
                ),
                (
                    "history_id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "adherence",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="effect_subject.adherence",
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
            ],
            options={
                "verbose_name": "historical Flucytosine Missed Dose",
                "verbose_name_plural": "historical Flucytosine Missed Doses",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="HistoricalFluconMissedDoses",
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
                    "day_missed",
                    models.IntegerField(
                        choices=[
                            (1, "Day 1"),
                            (2, "Day 2"),
                            (3, "Day 3"),
                            (4, "Day 4"),
                            (5, "Day 5"),
                            (6, "Day 6"),
                            (7, "Day 7"),
                            (8, "Day 8"),
                            (9, "Day 9"),
                            (10, "Day 10"),
                            (11, "Day 11"),
                            (12, "Day 12"),
                            (13, "Day 13"),
                            (14, "Day 14"),
                            (15, "Day 15"),
                        ],
                        verbose_name="Day missed:",
                    ),
                ),
                (
                    "missed_reason",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("toxicity", "Toxicity"),
                            ("missed", "Missed"),
                            ("REFUSED", "Refused"),
                            ("not_required", "Not required according to protocol"),
                            ("OTHER", "Other"),
                        ],
                        max_length=25,
                        verbose_name="Reason:",
                    ),
                ),
                (
                    "missed_reason_other",
                    edc_model_fields.fields.other_charfield.OtherCharField(
                        blank=True,
                        max_length=35,
                        null=True,
                        verbose_name="If other, please specify ...",
                    ),
                ),
                (
                    "history_id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "adherence",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="effect_subject.adherence",
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
            ],
            options={
                "verbose_name": "historical Fluconazole Missed Dose",
                "verbose_name_plural": "historical Fluconazole Missed Doses",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="FlucytMissedDoses",
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
                    "day_missed",
                    models.IntegerField(
                        choices=[
                            (1, "Day 1"),
                            (2, "Day 2"),
                            (3, "Day 3"),
                            (4, "Day 4"),
                            (5, "Day 5"),
                            (6, "Day 6"),
                            (7, "Day 7"),
                            (8, "Day 8"),
                            (9, "Day 9"),
                            (10, "Day 10"),
                            (11, "Day 11"),
                            (12, "Day 12"),
                            (13, "Day 13"),
                            (14, "Day 14"),
                            (15, "Day 15"),
                        ],
                        verbose_name="Day missed:",
                    ),
                ),
                (
                    "missed_reason",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("toxicity", "Toxicity"),
                            ("missed", "Missed"),
                            ("REFUSED", "Refused"),
                            ("not_required", "Not required according to protocol"),
                            ("OTHER", "Other"),
                        ],
                        max_length=25,
                        verbose_name="Reason:",
                    ),
                ),
                (
                    "missed_reason_other",
                    edc_model_fields.fields.other_charfield.OtherCharField(
                        blank=True,
                        max_length=35,
                        null=True,
                        verbose_name="If other, please specify ...",
                    ),
                ),
                (
                    "doses_missed",
                    models.IntegerField(
                        choices=[
                            (1, "1 Dose"),
                            (2, "2 Doses"),
                            (3, "3 Doses"),
                            (4, "4 Doses"),
                        ],
                        verbose_name="Doses missed:",
                    ),
                ),
                (
                    "adherence",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="effect_subject.adherence",
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
            ],
            options={
                "verbose_name": "Flucytosine Missed Dose",
                "verbose_name_plural": "Flucytosine Missed Doses",
                "ordering": ("-modified", "-created"),
                "get_latest_by": "modified",
                "abstract": False,
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "unique_together": {("adherence", "day_missed")},
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("on_site", edc_sites.model_mixins.CurrentSiteManager()),
            ],
        ),
        migrations.CreateModel(
            name="FluconMissedDoses",
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
                    "day_missed",
                    models.IntegerField(
                        choices=[
                            (1, "Day 1"),
                            (2, "Day 2"),
                            (3, "Day 3"),
                            (4, "Day 4"),
                            (5, "Day 5"),
                            (6, "Day 6"),
                            (7, "Day 7"),
                            (8, "Day 8"),
                            (9, "Day 9"),
                            (10, "Day 10"),
                            (11, "Day 11"),
                            (12, "Day 12"),
                            (13, "Day 13"),
                            (14, "Day 14"),
                            (15, "Day 15"),
                        ],
                        verbose_name="Day missed:",
                    ),
                ),
                (
                    "missed_reason",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("toxicity", "Toxicity"),
                            ("missed", "Missed"),
                            ("REFUSED", "Refused"),
                            ("not_required", "Not required according to protocol"),
                            ("OTHER", "Other"),
                        ],
                        max_length=25,
                        verbose_name="Reason:",
                    ),
                ),
                (
                    "missed_reason_other",
                    edc_model_fields.fields.other_charfield.OtherCharField(
                        blank=True,
                        max_length=35,
                        null=True,
                        verbose_name="If other, please specify ...",
                    ),
                ),
                (
                    "adherence",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="effect_subject.adherence",
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
            ],
            options={
                "verbose_name": "Fluconazole Missed Dose",
                "verbose_name_plural": "Fluconazole Missed Doses",
                "ordering": ("-modified", "-created"),
                "get_latest_by": "modified",
                "abstract": False,
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "unique_together": {("adherence", "day_missed")},
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("on_site", edc_sites.model_mixins.CurrentSiteManager()),
            ],
        ),
    ]
