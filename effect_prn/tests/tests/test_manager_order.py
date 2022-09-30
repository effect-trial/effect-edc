from django.apps import apps as django_apps
from django.test import TestCase, tag
from edc_action_item.managers import ActionIdentifierModelManager
from edc_sites.models import CurrentSiteManager


class TestManagers(TestCase):
    @tag("1")
    def test_models(self):
        app_label = "effect_prn"
        app_config = django_apps.get_app_config("effect_prn")
        for model_cls in app_config.get_models():
            if "historical" not in model_cls._meta.label_lower:
                self.assertEqual(
                    model_cls._default_manager.__class__,
                    CurrentSiteManager,
                    msg=f"Model is {model_cls}",
                )
