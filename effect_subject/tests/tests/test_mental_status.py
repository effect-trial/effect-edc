from django.test import TestCase
from model_bakery import baker

from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin
from effect_subject.forms import MentalStatusForm


class TestMentalStatus(EffectTestCaseMixin, TestCase):
    def test_ok(self):
        subject_visit = self.get_subject_visit()
        obj = baker.make_recipe("effect_subject.mentalstatus", subject_visit=subject_visit)
        form = MentalStatusForm(instance=obj)
        form.is_valid()
