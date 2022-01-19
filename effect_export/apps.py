from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = "effect_export"
    verbose_name = "EFFECT: Export Data"
