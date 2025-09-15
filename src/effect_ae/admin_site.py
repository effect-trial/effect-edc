from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

effect_ae_admin = EdcAdminSite(name="effect_ae_admin", app_label=AppConfig.name)
