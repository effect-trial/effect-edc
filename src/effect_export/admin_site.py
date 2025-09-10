from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

effect_export_admin = EdcAdminSite(name="effect_export_admin", app_label=AppConfig.name)
