from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

effect_prn_admin = EdcAdminSite(name="effect_prn_admin", app_label=AppConfig.name)
