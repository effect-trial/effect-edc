from django.apps import apps as django_apps

EFFECT_AUDITOR = "EFFECT_AUDITOR"
EFFECT_CLINIC = "EFFECT_CLINIC"
EFFECT_CLINIC_SUPER = "EFFECT_CLINIC_SUPER"
EFFECT_EXPORT = "EFFECT_EXPORT"

clinic_codenames = []
screening_codenames = []


for app_config in django_apps.get_app_configs():
    if app_config.name in [
        "effect_lists",
    ]:
        for model_cls in app_config.get_models():
            for prefix in ["view"]:
                clinic_codenames.append(
                    f"{app_config.name}.{prefix}_{model_cls._meta.model_name}"
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
                    clinic_codenames.append(
                        f"{app_config.name}.{prefix}_{model_cls._meta.model_name}"
                    )
clinic_codenames.sort()

for app_config in django_apps.get_app_configs():
    if app_config.name in [
        "effect_screening",
    ]:
        for model_cls in app_config.get_models():
            if "historical" in model_cls._meta.label_lower:
                screening_codenames.append(
                    f"{app_config.name}.view_{model_cls._meta.model_name}"
                )
            else:
                for prefix in ["add", "change", "view", "delete"]:
                    screening_codenames.append(
                        f"{app_config.name}.{prefix}_{model_cls._meta.model_name}"
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
