from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

effect_screening_admin = EdcAdminSite(name="effect_screening_admin", app_label=AppConfig.name)
