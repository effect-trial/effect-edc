from django.apps import AppConfig as DjangoApponfig


class AppConfig(DjangoApponfig):
    name = "effect_auth"
    verbose_name = "EFFECT: Authentication and Permissions"
    default_auto_field = "django.db.models.BigAutoField"
