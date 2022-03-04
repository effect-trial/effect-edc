from django.test import TestCase, tag
from edc_constants.constants import NO, NOT_APPLICABLE, YES
from edc_visit_schedule.constants import DAY1
from model_bakery import baker

from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin
from effect_subject.forms.vital_signs_form import (
    VitalSignsForm,
    VitalSignsFormValidator,
)

from .mixins import ReportingFieldsetFormValidatorTestCaseMixin


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


@tag("vs")
class TestVitalSignsFormValidationBase(EffectTestCaseMixin, TestCase):

    form_validator_default_form_cls = VitalSignsFormValidator

    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit()

    def get_valid_vital_signs_data(self, visit_code: str = DAY1):
        self.subject_visit.appointment.visit_code = visit_code
        return {
            "subject_visit": self.subject_visit,
            "appointment": self.subject_visit.appointment,
            "report_datetime": self.subject_visit.report_datetime,
            "weight": 60.0,
            "weight_measured_or_est": "measured",
            "heart_rate": 60,
            "respiratory_rate": 14,
            "temperature": 37.0,
            "reportable_as_ae": NOT_APPLICABLE if visit_code == DAY1 else NO,
            "patient_admitted": NOT_APPLICABLE if visit_code == DAY1 else NO,
        }


@tag("vs")
class TestVitalSignsFormValidation(TestVitalSignsFormValidationBase):
    pass


@tag("vs")
class TestVitalSignsReportingFieldsetFormValidation(
    ReportingFieldsetFormValidatorTestCaseMixin, TestVitalSignsFormValidationBase
):
    default_cleaned_data = TestVitalSignsFormValidationBase.get_valid_vital_signs_data
