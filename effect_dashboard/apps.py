from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = "effect_dashboard"
    verbose_name = f"EFFECT: Dashboard"
    include_in_administration_section = False
