from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = "effect_visit_schedule"
    verbose_name = "EFFECT: Visit Schedule"
