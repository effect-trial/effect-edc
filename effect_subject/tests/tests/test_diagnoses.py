from django.test import TestCase, tag
from edc_constants.constants import NO, NOT_APPLICABLE
from edc_visit_schedule.constants import DAY1
from model_bakery import baker

from effect_lists.models import Dx
from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin
from effect_subject.forms.diagnoses_form import DiagnosesForm, DiagnosesFormValidator
from effect_visit_schedule.constants import DAY14

from .mixins import ReportingFieldsetBaselineTestCaseMixin


@tag("dx")
class TestDiagnoses(EffectTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit()

    def test_ok(self):
        subject_visit = self.subject_visit
        obj = baker.make_recipe(
            "effect_subject.diagnoses",
            subject_visit=subject_visit,
        )
        form = DiagnosesForm(instance=obj)
        form.is_valid()


@tag("dx")
class TestDiagnosesFormValidationBase(EffectTestCaseMixin, TestCase):

    form_validator_default_form_cls = DiagnosesFormValidator

    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit()

    def get_valid_diagnoses_data(self, visit_code: str = DAY1):
        self.subject_visit.appointment.visit_code = visit_code
        return {
            "subject_visit": self.subject_visit,
            "appointment": self.subject_visit.appointment,
            "report_datetime": self.subject_visit.report_datetime,
            "gi_side_effects": NO,
            "gi_side_effects_details": "",
            "has_diagnoses": NO,
            "diagnoses": Dx.objects.filter(name=""),  # TODO check:
            "diagnoses_other": "",
            "reportable_as_ae": NOT_APPLICABLE if visit_code == DAY1 else NO,
            "patient_admitted": NOT_APPLICABLE if visit_code == DAY1 else NO,
        }

    def test_baseline_valid_diagnoses_data_valid(self):
        cleaned_data = self.get_valid_diagnoses_data(visit_code=DAY1)
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_d14_valid_diagnoses_data_valid(self):
        cleaned_data = self.get_valid_diagnoses_data(visit_code=DAY14)
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )


@tag("dx")
class TestDiagnosesFormValidation(TestDiagnosesFormValidationBase):
    pass


@tag("dx")
class TestDiagnosesReportingFieldsetFormValidation(
    ReportingFieldsetBaselineTestCaseMixin, TestDiagnosesFormValidationBase
):
    default_cleaned_data = TestDiagnosesFormValidationBase.get_valid_diagnoses_data
