from django.test import TestCase, tag
from edc_constants.constants import NO, NOT_APPLICABLE
from model_bakery import baker

from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin
from effect_subject.forms.vital_signs_form import (
    VitalSignsForm,
    VitalSignsFormValidator,
)
from effect_visit_schedule.constants import DAY01, DAY14

from .mixins import (
    ReportingFieldsetBaselineTestCaseMixin,
    ReportingFieldsetDay14TestCaseMixin,
)


@tag("vs")
class TestVitalSigns(EffectTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit()

    def test_ok(self):
        subject_visit = self.subject_visit
        obj = baker.make_recipe(
            "effect_subject.vitalsigns",
            subject_visit=subject_visit,
            temperature=37.0,
        )
        form = VitalSignsForm(instance=obj)
        form.is_valid()
