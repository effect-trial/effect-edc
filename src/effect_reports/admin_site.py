from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

effect_reports_admin = EdcAdminSite(name="effect_reports_admin", app_label=AppConfig.name)
