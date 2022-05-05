from django.test import TestCase, tag
from edc_constants.constants import NO, NOT_APPLICABLE, YES
from model_bakery import baker

from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin
from effect_subject.forms import MentalStatusForm
from effect_subject.forms.mental_status_form import MentalStatusFormValidator
from effect_subject.tests.tests.mixins import (
    ReportingFieldsetBaselineTestCaseMixin,
    ReportingFieldsetDay14TestCaseMixin,
)
from effect_visit_schedule.constants import DAY01, DAY14


@tag("ms")
class TestMentalStatus(EffectTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit()

    def test_ok(self):
        subject_visit = self.subject_visit
        obj = baker.make_recipe("effect_subject.mentalstatus", subject_visit=subject_visit)
        form = MentalStatusForm(instance=obj)
        form.is_valid()


@tag("ms")
class TestMentalStatusFormValidationBase(EffectTestCaseMixin, TestCase):

    form_validator_default_form_cls = MentalStatusFormValidator

    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit()

    def get_valid_mental_status_data(self, visit_code: str = DAY01):
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
            "reportable_as_ae": NOT_APPLICABLE if visit_code == DAY01 else NO,
            "patient_admitted": NOT_APPLICABLE if visit_code == DAY01 else NO,
        }


@tag("ms")
class TestMentalStatusFormValidation(TestMentalStatusFormValidationBase):
    def test_baseline_valid_mental_status_data_valid(self):
        cleaned_data = self.get_valid_mental_status_data(visit_code=DAY01)
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_d14_valid_mental_status_data_valid(self):
        cleaned_data = self.get_valid_mental_status_data(visit_code=DAY14)
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_seizures_at_baseline_raises_error(self):
        cleaned_data = self.get_valid_mental_status_data(visit_code=DAY01)
        cleaned_data.update({"recent_seizure": YES})
        self.assertFormValidatorError(
            field="recent_seizure",
            expected_msg="Invalid. Cannot have had a recent seizure at baseline",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_gcs_lt_15_at_baseline_raises_error(self):
        cleaned_data = self.get_valid_mental_status_data(visit_code=DAY01)
        for gcs in [3, 14]:
            with self.subTest(gcs=gcs):
                cleaned_data.update({"glasgow_coma_score": gcs})
                self.assertFormValidatorError(
                    field="glasgow_coma_score",
                    expected_msg="Invalid. GCS cannot be less than 15 at baseline",
                    form_validator=self.validate_form_validator(cleaned_data),
                )

    def test_seizures_at_d14_ok(self):
        cleaned_data = self.get_valid_mental_status_data(visit_code=DAY14)
        cleaned_data.update({"recent_seizure": YES})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_gcs_lt_15_at_d14_ok(self):
        cleaned_data = self.get_valid_mental_status_data(visit_code=DAY14)
        for gcs in [3, 14]:
            with self.subTest(gcs=gcs):
                cleaned_data.update({"glasgow_coma_score": gcs})
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(cleaned_data)
                )


@tag("ms")
class TestMentalStatusReportingFieldsetFormValidation(
    ReportingFieldsetBaselineTestCaseMixin,
    ReportingFieldsetDay14TestCaseMixin,
    TestMentalStatusFormValidationBase,
):
    default_cleaned_data = TestMentalStatusFormValidationBase.get_valid_mental_status_data
