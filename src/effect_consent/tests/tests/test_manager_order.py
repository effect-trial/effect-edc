from django.apps import apps as django_apps
from django.test import TestCase
from edc_identifier.managers import SubjectIdentifierManager
from edc_model.models.historical_records import SerializableModelManager

from effect_consent.models import SubjectConsentUpdateV2
from effect_consent.models.subject_consent import SubjectConsentManager


class TestManagers(TestCase):
    def test_model_default_manager_names(self):
        app_label = "effect_consent"
        app_config = django_apps.get_app_config(app_label)
        for model_cls in app_config.get_models():
            if model_cls._meta.proxy:
                continue
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
        app_label = "effect_consent"
        app_config = django_apps.get_app_config(app_label)
        for model_cls in app_config.get_models():
            if model_cls._meta.proxy:
                continue
            elif model_cls == SubjectConsentUpdateV2:
                continue
            elif "historical" in model_cls._meta.label_lower:
                self.assertEqual(
                    model_cls._default_manager.__class__,
                    SerializableModelManager,
                    msg=f"Model is {model_cls}",
                )
            elif model_cls._meta.label_lower == f"{app_label}.subjectconsent":
                self.assertEqual(
                    model_cls._default_manager.__class__,
                    SubjectConsentManager,
                    msg=f"Model is {model_cls}",
                )
            elif model_cls._meta.label_lower == f"{app_label}.subjectreconsent":
                self.assertEqual(
                    model_cls._default_manager.__class__,
                    SubjectIdentifierManager,
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
