from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

effect_consent_admin = EdcAdminSite(
    name="effect_consent_admin", app_label=AppConfig.name
)
