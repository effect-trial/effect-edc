from django.test import TestCase
from model_bakery import baker

from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin
from effect_subject.forms.vital_signs_form import VitalSignsForm


class TestVitalSigns(EffectTestCaseMixin, TestCase):
    def test_ok(self):
        subject_visit = self.get_subject_visit()
        obj = baker.make_recipe(
            "effect_subject.vitalsigns",
            subject_visit=subject_visit,
            temperature=37.0,
        )
        form = VitalSignsForm(instance=obj)
        form.is_valid()
