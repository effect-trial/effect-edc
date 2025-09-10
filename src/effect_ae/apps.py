from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = "effect_ae"
    verbose_name = "EFFECT: Adverse Events"
    include_in_administration_section = False
    has_exportable_data = True
    default_auto_field = "django.db.models.BigAutoField"
