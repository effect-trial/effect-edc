from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

effect_subject_admin = EdcAdminSite(
    name="effect_subject_admin", app_label=AppConfig.name
)
