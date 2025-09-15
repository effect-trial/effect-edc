import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "effect_edc.settings.debug")

application = get_asgi_application()
