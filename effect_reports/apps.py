from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = "effect_reports"
    verbose_name = "EFFECT: Reports"
    include_in_administration_section = True
