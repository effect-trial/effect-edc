from django.test import TestCase, tag
from edc_constants.constants import NO, NOT_APPLICABLE
from edc_visit_schedule.constants import DAY1
from model_bakery import baker

from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin
from effect_subject.forms import MentalStatusForm
from effect_subject.forms.mental_status_form import MentalStatusFormValidator
from effect_subject.tests.tests.mixins import (
    ReportingFieldsetFormValidatorTestCaseMixin,
)


@tag("ms")
class TestMentalStatus(EffectTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit()

    def test_ok(self):
        subject_visit = self.subject_visit
        obj = baker.make_recipe(
            "effect_subject.mentalstatus", subject_visit=subject_visit
        )
        form = MentalStatusForm(instance=obj)
        form.is_valid()


@tag("ms")
class TestMentalStatusFormValidationBase(EffectTestCaseMixin, TestCase):

    form_validator_default_form_cls = MentalStatusFormValidator

    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit()

    def get_valid_mental_status_data(self, visit_code: str = DAY1):
        self.subject_visit.appointment.visit_code = visit_code
        return {
            "subject_visit": self.subject_visit,
            "appointment": self.subject_visit.appointment,
            "report_datetime": self.subject_visit.report_datetime,
            "recent_seizure": NO,
            "behaviour_change": NO,
            "confusion": NO,
            "modified_rankin_score": "0",
            "ecog_score": "0",
            "glasgow_coma_score": 15,
            "reportable_as_ae": NOT_APPLICABLE if visit_code == DAY1 else NO,
            "patient_admitted": NOT_APPLICABLE if visit_code == DAY1 else NO,
        }


@tag("ms")
class TestMentalStatusFormValidation(TestMentalStatusFormValidationBase):
    pass


@tag("ms")
class TestMentalStatusReportingFieldsetFormValidation(
    ReportingFieldsetFormValidatorTestCaseMixin, TestMentalStatusFormValidationBase
):
    default_cleaned_data = (
        TestMentalStatusFormValidationBase.get_valid_mental_status_data
    )
