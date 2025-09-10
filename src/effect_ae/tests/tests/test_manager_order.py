from django.apps import apps as django_apps
from django.db.models.manager import Manager
from django.test import TestCase
from edc_action_item.managers import ActionIdentifierModelManager
from edc_adverse_event.model_mixins import DeathReportTmgSecondManager
from edc_adverse_event.model_mixins.death_report import DeathReportTmgManager
from edc_model.models.historical_records import SerializableModelManager


class TestManagers(TestCase):
    def test_model_default_manager_names(self):
        app_label = "effect_ae"
        app_config = django_apps.get_app_config(app_label)
        for model_cls in app_config.get_models():
            if "historical" not in model_cls._meta.label_lower:
                self.assertEqual(
                    model_cls._meta.default_manager.name,
                    "objects",
                    msg=f"Model is {model_cls}",
                )

    def test_models(self):
        app_label = "effect_ae"
        app_config = django_apps.get_app_config(app_label)
        django_manager_managed = [f"{app_label}.aelocalreview", f"{app_label}.aesponsorreview"]
        action_identifier_managed = [
            f"{app_label}.aefollowup",
            f"{app_label}.aeinitial",
            f"{app_label}.aesusar",
            f"{app_label}.aetmg",
            f"{app_label}.deathreport",
        ]
        for model_cls in app_config.get_models():
            if "historical" in model_cls._meta.label_lower:
                self.assertEqual(
                    model_cls._default_manager.__class__,
                    SerializableModelManager,
                    msg=f"Model is {model_cls}",
                )
            elif model_cls._meta.label_lower == f"{app_label}.deathreporttmg":
                self.assertEqual(
                    model_cls._default_manager.__class__,
                    DeathReportTmgManager,
                    msg=f"Model is {model_cls}",
                )
            elif model_cls._meta.label_lower == f"{app_label}.deathreporttmgsecond":
                self.assertEqual(
                    model_cls._default_manager.__class__,
                    DeathReportTmgSecondManager,
                    msg=f"Model is {model_cls}",
                )
            elif model_cls._meta.label_lower in django_manager_managed:
                self.assertEqual(
                    model_cls._default_manager.__class__,
                    Manager,
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
