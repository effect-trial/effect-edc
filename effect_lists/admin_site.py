from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

effect_lists_admin = EdcAdminSite(name="effect_lists_admin", app_label=AppConfig.name)
