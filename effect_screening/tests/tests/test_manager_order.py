from django.apps import apps as django_apps
from django.test import TestCase
from edc_model.models.historical_records import SerializableModelManager
from edc_screening.model_mixins import ScreeningManager


class TestManagers(TestCase):
    def test_model_default_manager_names(self):
        app_label = "effect_screening"
        app_config = django_apps.get_app_config(app_label)
        for model_cls in app_config.get_models():
            if "historical" in model_cls._meta.label_lower:
                self.assertIsNone(
                    model_cls._meta.default_manager_name,
                    msg=f"Model is {model_cls}",
                )
            else:
                self.assertEqual(
                    model_cls._meta.default_manager_name,
                    "objects",
                    msg=f"Model is {model_cls}",
                )

    def test_models(self):
        app_label = "effect_screening"
        app_config = django_apps.get_app_config(app_label)
        for model_cls in app_config.get_models():
            if "historical" in model_cls._meta.label_lower:
                self.assertEqual(
                    model_cls._default_manager.__class__,
                    SerializableModelManager,
                    msg=f"Model is {model_cls}",
                )
            elif model_cls._meta.label_lower == f"{app_label}.subjectscreening":
                self.assertEqual(
                    model_cls._default_manager.__class__,
                    ScreeningManager,
                    msg=f"Model is {model_cls}",
                )
            else:
                self.fail(
                    msg=(
                        "Unexpectedly got this far. Expected model to have "
                        "matched with test assertion declared above. "
                        "Have you defined a case for it in this test? "
                        f"Model is {model_cls}"
                    )
                )
