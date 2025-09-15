from __future__ import annotations

from typing import TYPE_CHECKING

from django.apps import apps as django_apps
from edc_auth.get_app_codenames import get_app_codenames

if TYPE_CHECKING:
    from django.apps import AppConfig

EFFECT_AUDITOR = "EFFECT_AUDITOR"
EFFECT_CLINIC = "EFFECT_CLINIC"
EFFECT_CLINIC_SUPER = "EFFECT_CLINIC_SUPER"
EFFECT_EXPORT = "EFFECT_EXPORT"
EFFECT_REPORTS = "EFFECT_REPORTS"
EFFECT_REPORTS_AUDIT = "EFFECT_REPORTS_AUDIT"

clinic_codenames = []
screening_codenames = []

reports_codenames = get_app_codenames("effect_reports")


def format_as_codename(prefix: str, model_cls, app_config: AppConfig):
    return f"{app_config.name}.{prefix}_{model_cls._meta.model_name}"


for app_config in django_apps.get_app_configs():
    if app_config.name in ["effect_lists"]:
        clinic_codenames.extend(
            [
                format_as_codename("view", model_cls, app_config)
                for model_cls in app_config.get_models()
            ]
        )

for app_config in django_apps.get_app_configs():
    if app_config.name in [
        "effect_prn",
        "effect_subject",
        "effect_consent",
        "effect_screening",
    ]:
        for model_cls in app_config.get_models():
            if "historical" in model_cls._meta.label_lower:
                clinic_codenames.append(f"{app_config.name}.view_{model_cls._meta.model_name}")
            else:
                for prefix in ["add", "change", "view", "delete"]:
                    clinic_codenames.extend(
                        [format_as_codename(prefix, model_cls, app_config)]
                    )
clinic_codenames.sort()

for app_config in django_apps.get_app_configs():
    if app_config.name in [
        "effect_screening",
    ]:
        for model_cls in app_config.get_models():
            if "historical" in model_cls._meta.label_lower:
                screening_codenames.append(format_as_codename("view", model_cls, app_config))
            else:
                for prefix in ["add", "change", "view", "delete"]:
                    screening_codenames.extend(
                        [format_as_codename(prefix, model_cls, app_config)]
                    )
screening_codenames.sort()


ae_local_reviewer = [
    "effect_subject.add_aelocalreview",
    "effect_subject.change_aelocalreview",
    "effect_subject.delete_aelocalreview",
    "effect_subject.view_aelocalreview",
    "effect_subject.view_historicalaelocalreview",
]
ae_sponsor_reviewer = [
    "effect_subject.add_aesponsorreview",
    "effect_subject.change_aesponsorreview",
    "effect_subject.delete_aesponsorreview",
    "effect_subject.view_aesponsorreview",
    "effect_subject.view_historicalaesponsorreview",
]
