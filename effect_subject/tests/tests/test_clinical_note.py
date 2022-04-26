from django.test import TestCase, tag
from edc_constants.constants import NO, YES
from edc_visit_schedule.constants import DAY1

from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin
from effect_subject.forms.clinical_note_form import ClinicalNoteFormValidator


@tag("cn")
class TestClinicalNoteFormValidation(EffectTestCaseMixin, TestCase):
    form_validator_default_form_cls = ClinicalNoteFormValidator

    def get_cleaned_data(self, visit_code: str):
        subject_visit = self.get_subject_visit(visit_code=visit_code)
        return {
            "subject_visit": subject_visit,
            "report_datetime": subject_visit.report_datetime,
            "has_comment": NO,
            "comments": None,
        }

    def test_clean_data_valid(self):
        cleaned_data = self.get_cleaned_data(visit_code=DAY1)
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_has_comment_yes_comment_no_raises(self):
        cleaned_data = self.get_cleaned_data(visit_code=DAY1)
        cleaned_data.update(has_comment=YES, comments=None)

        self.assertFormValidatorError(
            field="comments",
            expected_msg="This field is required",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_has_comment_no_comment_yes_raises(self):
        cleaned_data = self.get_cleaned_data(visit_code=DAY1)
        cleaned_data.update(has_comment=NO, comments="Data blahh blahh")

        self.assertFormValidatorError(
            field="comments",
            expected_msg="This field is not required",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_has_comment_no_comment_none(self):
        cleaned_data = self.get_cleaned_data(visit_code=DAY1)
        cleaned_data.update(has_comment=NO, comments=None)

        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )
