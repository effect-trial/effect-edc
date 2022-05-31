from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_consent.constants import CONSENT_WITHDRAWAL
from edc_constants.constants import NO, NOT_APPLICABLE, OTHER, YES
from edc_utils import get_utcnow

from effect_prn.constants import CARE_TRANSFERRED_OUT, LATE_EXCLUSION_OTHER
from effect_prn.form_validators import EndOfStudyFormValidator
from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin


@tag("eos")
class TestEndOfStudyFormValidation(EffectTestCaseMixin, TestCase):

    form_validator_default_form_cls = EndOfStudyFormValidator

    def get_cleaned_data(self):
        return {
            "offschedule_datetime": get_utcnow(),
            "last_followup_date": get_utcnow() - relativedelta(days=5),
            "cm_admitted": NO,
            "cm_admitted_cnt": None,
            "offschedule_reason": "completed_6m_followup",
            "offschedule_reason_other": None,
            "withdrawal_consent_reasons": None,
            "late_exclusion_other": None,
            "transferred_consent": None,
        }

    def test_cleaned_data_ok(self):
        cleaned_data = self.get_cleaned_data()
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_cm_admitted_yes_cm_admitted_cnt_none(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(cm_admitted=YES, cm_admitted_cnt=None)

        self.assertFormValidatorError(
            field="cm_admitted_cnt",
            expected_msg="This field is required",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_cm_admitted_no_cm_admitted_cnt(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(cm_admitted=NO, cm_admitted_cnt=1)

        self.assertFormValidatorError(
            field="cm_admitted_cnt",
            expected_msg="This field is not required",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_offschedule_reason_other_offschedule_reason_other_none(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(offschedule_reason=OTHER, offschedule_reason_other=None)

        self.assertFormValidatorError(
            field="offschedule_reason_other",
            expected_msg="This field is required",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_offschedule_reason_offschedule_reason_other_true(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            offschedule_reason="completed_6m_followup", offschedule_reason_other="None"
        )

        self.assertFormValidatorError(
            field="offschedule_reason_other",
            expected_msg="This field is not required",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_offschedule_reason_late_exclusion_other_true(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(offschedule_reason=LATE_EXCLUSION_OTHER, late_exclusion_other=None)

        self.assertFormValidatorError(
            field="late_exclusion_other",
            expected_msg="This field is required",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_offschedule_reason_late_exclusion_other_false(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            offschedule_reason="completed_6m_followup", late_exclusion_other="Some data"
        )

        self.assertFormValidatorError(
            field="late_exclusion_other",
            expected_msg="This field is not required",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_offschedule_reason_consent_withdrawn_true(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            offschedule_reason=CONSENT_WITHDRAWAL, withdrawal_consent_reasons=None
        )

        self.assertFormValidatorError(
            field="withdrawal_consent_reasons",
            expected_msg="This field is required",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_offschedule_reason_consent_withdrawn_false(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            offschedule_reason="completed_6m_followup", withdrawal_consent_reasons="Some data"
        )

        self.assertFormValidatorError(
            field="withdrawal_consent_reasons",
            expected_msg="This field is not required",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_offschedule_reason_care_transferred_out_true(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(offschedule_reason=CARE_TRANSFERRED_OUT, transferred_consent=None)

        self.assertFormValidatorError(
            field="transferred_consent",
            expected_msg="This field is required",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_offschedule_reason_care_transferred_out_true_transferred_consent_na(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            offschedule_reason=CARE_TRANSFERRED_OUT, transferred_consent=NOT_APPLICABLE
        )

        self.assertFormValidatorError(
            field="transferred_consent",
            expected_msg="This field is required",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_offschedule_reason_care_transferred_out_false(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            offschedule_reason="completed_6m_followup", transferred_consent=YES
        )

        self.assertFormValidatorError(
            field="transferred_consent",
            expected_msg="This field is not required",
            form_validator=self.validate_form_validator(cleaned_data),
        )
