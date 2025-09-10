from django.apps import apps as django_apps
from django.test import TestCase
from edc_action_item.managers import ActionIdentifierModelManager
from edc_identifier.managers import SubjectIdentifierManager
from edc_model.models.historical_records import SerializableModelManager
from edc_visit_schedule.model_mixins.on_schedule_model_mixin import OnScheduleManager


class TestManagers(TestCase):
    def test_model_default_manager_names(self):
        app_label = "effect_prn"
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
        app_label = "effect_prn"
        app_config = django_apps.get_app_config(app_label)
        on_schedule_managed = [f"{app_label}.onschedule"]
        subject_identifier_managed = [f"{app_label}.endofstudy"]
        action_identifier_managed = [
            f"{app_label}.hospitalization",
            f"{app_label}.losstofollowup",
            f"{app_label}.protocoldeviationviolation",
        ]
        for model_cls in app_config.get_models():
            if "historical" in model_cls._meta.label_lower:
                self.assertEqual(
                    model_cls._default_manager.__class__,
                    SerializableModelManager,
                    msg=f"Model is {model_cls}",
                )
            elif model_cls._meta.label_lower in on_schedule_managed:
                self.assertEqual(
                    model_cls._default_manager.__class__,
                    OnScheduleManager,
                    msg=f"Model is {model_cls}",
                )
            elif model_cls._meta.label_lower in subject_identifier_managed:
                self.assertEqual(
                    model_cls._default_manager.__class__,
                    SubjectIdentifierManager,
                    msg=f"Model is {model_cls}",
                )
            elif model_cls._meta.label_lower in action_identifier_managed:
                self.assertEqual(
                    model_cls._default_manager.__class__,
                    ActionIdentifierModelManager,
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
