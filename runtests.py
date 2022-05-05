#!/usr/bin/env python
import logging
import sys
from datetime import datetime
from os.path import abspath, dirname, join

import django
from dateutil.tz import gettz
from django.conf import settings
from django.test.runner import DiscoverRunner
from edc_test_utils import DefaultTestSettings
from multisite import SiteID

app_name = "effect_edc"
base_dir = dirname(abspath(__file__))


DEFAULT_SETTINGS = DefaultTestSettings(
    calling_file=__file__,
    EDC_RANDOMIZATION_REGISTER_DEFAULT_RANDOMIZER=True,
    EDC_RANDOMIZATION_ASSIGNMENT_MAP={"control": 1, "intervention": 2},
    ROOT_URLCONF="effect_edc.urls",
    EDC_AUTH_CODENAMES_WARN_ONLY=True,
    EDC_DX_REVIEW_LIST_MODEL_APP_LABEL="edc_dx_review",
    BASE_DIR=base_dir,
    APP_NAME=app_name,
    SITE_ID=SiteID(default=200),
    SENTRY_ENABLED=False,
    INDEX_PAGE="localhost:8000",
    EXPORT_FOLDER=join(base_dir, "tests", "export"),
    SUBJECT_APP_LABEL="effect_subject",
    SUBJECT_SCREENING_MODEL="effect_screening.subjectscreening",
    SUBJECT_VISIT_MODEL="effect_subject.subjectvisit",
    SUBJECT_VISIT_MISSED_MODEL="effect_subject.subjectvisitmissed",
    SUBJECT_CONSENT_MODEL="effect_consent.subjectconsent",
    SUBJECT_REQUISITION_MODEL="effect_subject.subjectrequisition",
    EDC_BLOOD_RESULTS_MODEL_APP_LABEL="effect_subject",
    DEFENDER_ENABLED=False,
    DJANGO_LAB_DASHBOARD_REQUISITION_MODEL="effect_subject.subjectrequisition",
    ADVERSE_EVENT_ADMIN_SITE="effect_ae_admin",
    EDC_DX_LABELS=dict(hiv="HIV", dm="Diabetes", htn="Hypertension", chol="High Cholesterol"),
    ADVERSE_EVENT_APP_LABEL="effect_ae",
    EDC_NAVBAR_DEFAULT="effect_dashboard",
    EDC_PROTOCOL_STUDY_OPEN_DATETIME=datetime(2019, 4, 30, 0, 0, 0, tzinfo=gettz("UTC")),
    EDC_PROTOCOL_STUDY_CLOSE_DATETIME=datetime(2023, 12, 31, 23, 59, 59, tzinfo=gettz("UTC")),
    DJANGO_LANGUAGES=dict(
        en="English",
        lg="Luganda",
        rny="Runyankore",
    ),
    DASHBOARD_BASE_TEMPLATES=dict(
        edc_base_template="edc_dashboard/base.html",
        listboard_base_template="effect_edc/base.html",
        dashboard_base_template="effect_edc/base.html",
        screening_listboard_template="effect_dashboard/screening/listboard.html",
        subject_listboard_template="effect_dashboard/subject/listboard.html",
        subject_dashboard_template="effect_dashboard/subject/dashboard.html",
        subject_review_listboard_template="edc_review_dashboard/subject_review_listboard.html",
    ),
    ETC_DIR=join(base_dir, "effect_edc", "tests", "etc"),
    EDC_BOOTSTRAP=3,
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    EMAIL_CONTACTS={
        "data_request": "someone@example.com",
        "data_manager": "someone@example.com",
        "tmg": "someone@example.com",
    },
    EMAIL_ENABLED=True,
    HOLIDAY_FILE=join(base_dir, "effect_edc", "tests", "holidays.csv"),
    LIVE_SYSTEM=False,
    EDC_RANDOMIZATION_LIST_PATH=join(base_dir, "effect_edc", "tests", "etc"),
    EDC_SITES_MODULE_NAME="effect_sites",
    INSTALLED_APPS=[
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.contrib.sites",
        "django_crypto_fields.apps.AppConfig",
        "django_revision.apps.AppConfig",
        # "debug_toolbar",
        "django_extensions",
        "django_celery_results",
        "django_celery_beat",
        "logentry_admin",
        "simple_history",
        "storages",
        # "corsheaders",
        "rest_framework",
        "rest_framework.authtoken",
        # "django_collect_offline.apps.AppConfig",
        # "django_collect_offline_files.apps.AppConfig",
        "edc_action_item.apps.AppConfig",
        "edc_adverse_event.apps.AppConfig",
        "edc_appointment.apps.AppConfig",
        "edc_auth.apps.AppConfig",
        "edc_model_wrapper.apps.AppConfig",
        "edc_crf.apps.AppConfig",
        "edc_data_manager.apps.AppConfig",
        "edc_consent.apps.AppConfig",
        "edc_device.apps.AppConfig",
        "edc_dashboard.apps.AppConfig",
        "edc_export.apps.AppConfig",
        "edc_facility.apps.AppConfig",
        "edc_fieldsets.apps.AppConfig",
        "edc_form_validators.apps.AppConfig",
        "edc_reportable.apps.AppConfig",
        "edc_lab.apps.AppConfig",
        "edc_lab_dashboard.apps.AppConfig",
        "edc_label.apps.AppConfig",
        "edc_locator.apps.AppConfig",
        "edc_reference.apps.AppConfig",
        "edc_reports.apps.AppConfig",
        "edc_identifier.apps.AppConfig",
        "edc_metadata.apps.AppConfig",
        "edc_model_admin.apps.AppConfig",
        "edc_navbar.apps.AppConfig",
        "edc_notification.apps.AppConfig",
        "edc_offstudy.apps.AppConfig",
        "edc_protocol_violation.apps.AppConfig",
        "edc_visit_tracking.apps.AppConfig",
        "edc_visit_schedule.apps.AppConfig",
        "edc_pdutils.apps.AppConfig",
        "edc_pharmacy.apps.AppConfig",
        # "edc_pharmacy_dashboard.apps.AppConfig",
        "edc_prn.apps.AppConfig",
        "edc_randomization.apps.AppConfig",
        "edc_registration.apps.AppConfig",
        "edc_screening.apps.AppConfig",
        "edc_subject_dashboard.apps.AppConfig",
        "edc_timepoint.apps.AppConfig",
        "edc_list_data.apps.AppConfig",
        "edc_review_dashboard.apps.AppConfig",
        "edc_sites.apps.AppConfig",
        "edc_dx_review.apps.AppConfig",
        "edc_dx.apps.AppConfig",
        "edc_refusal.apps.AppConfig",
        "edc_unblinding.apps.AppConfig",
        "effect_auth.apps.AppConfig",
        "effect_consent.apps.AppConfig",
        "effect_lists.apps.AppConfig",
        "effect_dashboard.apps.AppConfig",
        "effect_labs.apps.AppConfig",
        "effect_subject.apps.AppConfig",
        "effect_visit_schedule.apps.AppConfig",
        "effect_ae.apps.AppConfig",
        "effect_prn.apps.AppConfig",
        "effect_export.apps.AppConfig",
        "effect_screening.apps.AppConfig",
        "effect_edc.apps.AppConfig",
    ],
    add_dashboard_middleware=True,
    add_lab_dashboard_middleware=True,
    add_adverse_event_dashboard_middleware=True,
).settings


def main():
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)
    django.setup()
    tags = [t.split("=")[1] for t in sys.argv if t.startswith("--tag")]
    failfast = True if [t for t in sys.argv if t == "--failfast"] else False
    failures = DiscoverRunner(failfast=failfast, tags=tags).run_tests(
        [
            # "tests",
            # "effect_ae.tests",
            # "effect_dashboard.tests",
            # "effect_edc.tests",
            # "effect_labs.tests",
            # "effect_lists.tests",
            # "effect_prn.tests",
            # "effect_screening.tests",
            # "effect_subject.tests",
        ]
    )
    sys.exit(bool(failures))


if __name__ == "__main__":
    logging.basicConfig()
    main()
