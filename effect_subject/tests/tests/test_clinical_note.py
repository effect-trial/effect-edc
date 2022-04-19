from django.test import TestCase, tag
from edc_constants.constants import NO, YES
from edc_visit_schedule.constants import DAY1

from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin
from effect_subject.forms.clinical_note_form import ClinicalNoteFormValidator


@tag("cn")
class TestVitalSigns(EffectTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit()


@tag("cn")
class TestClinicalNoteFormValidationBase(EffectTestCaseMixin, TestCase):

    form_validator_default_form_cls = ClinicalNoteFormValidator

    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit()

    def get_clinical_note_data(self, visit_code: str = DAY1):
        self.subject_visit.appointment.visit_code = visit_code
        return {
            "subject_visit": self.subject_visit,
            "appointment": self.subject_visit.appointment,
            "report_datetime": self.subject_visit.report_datetime,
            "has_comment": NO,
            "comments": None,
        }


@tag("cn")
class TestClinicalNoteFormValidation(TestClinicalNoteFormValidationBase):
    def test_clinical_note_data_valid(self):
        cleaned_data = self.get_clinical_note_data(visit_code=DAY1)
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )
