from django.apps import apps as django_apps
from django.test import TestCase
from edc_lab.managers import RequisitionManager
from edc_model.models.historical_records import SerializableModelManager
from edc_visit_tracking.managers import CrfModelManager

from effect_subject.models.adherence.missed_doses_manager import MissedDosesManager
from effect_subject.models.subject_visit import VisitModelManager


class TestManagers(TestCase):
    def test_model_default_manager_names(self):
        app_label = "effect_subject"
        app_config = django_apps.get_app_config(app_label)
        for model_cls in app_config.get_models():
            if "historical" in model_cls._meta.label_lower or model_cls._meta.proxy:
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
        app_label = "effect_subject"
        app_config = django_apps.get_app_config(app_label)
        inlines = [f"{app_label}.fluconmisseddoses", f"{app_label}.flucytmisseddoses"]
        requisition_model = f"{app_label}.subjectrequisition"
        visit_model = f"{app_label}.subjectvisit"
        for model_cls in app_config.get_models():
            if "historical" in model_cls._meta.label_lower:
                self.assertEqual(
                    model_cls._default_manager.__class__,
                    SerializableModelManager,
                    msg=f"Model is {model_cls}",
                )
            elif model_cls._meta.label_lower in inlines:
                self.assertEqual(
                    model_cls._default_manager.__class__,
                    MissedDosesManager,
                    msg=f"Model is {model_cls}",
                )
            elif model_cls._meta.label_lower == visit_model:
                self.assertEqual(
                    model_cls._default_manager.__class__,
                    VisitModelManager,
                    msg=f"Model is {model_cls}",
                )
            elif model_cls._meta.label_lower == requisition_model:
                self.assertEqual(
                    model_cls._default_manager.__class__,
                    RequisitionManager,
                    msg=f"Model is {model_cls}",
                )
            else:
                self.assertEqual(
                    model_cls._default_manager.__class__,
                    CrfModelManager,
                    msg=f"Model is {model_cls}",
                )
