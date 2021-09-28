from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = "effect_screening"
    verbose_name = "EFFECT: Screening"
