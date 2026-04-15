from clinicedc_constants import NOT_APPLICABLE, OPEN
from django.forms import ValidationError
from django.test import TestCase, tag
from edc_form_validators import FormValidatorTestCaseMixin
from edc_protocol_incident.constants import DEVIATION

from effect_prn.constants import REMAIN_ON_STUDY_MODIFIED
from effect_prn.form_validators import ProtocolDeviationViolationFormValidator


@tag("pdv")
class TestProtocolDeviationViolationFormValidation(FormValidatorTestCaseMixin, TestCase):
    form_validator_cls = ProtocolDeviationViolationFormValidator

    @staticmethod
    def get_cleaned_data() -> dict:
        # Use report_type=DEVIATION and report_status=OPEN so the VIOLATION-
        # and CLOSED-gated checks are all skipped; only validate_action runs.
        return {
            "report_type": DEVIATION,
            "report_status": OPEN,
            "safety_impact": NOT_APPLICABLE,
            "study_outcomes_impact": NOT_APPLICABLE,
            "violation_type": NOT_APPLICABLE,
            "violation_type_other": "",
            "violation_datetime": None,
            "violation_description": "",
            "violation_reason": "",
            "corrective_action_datetime": None,
            "corrective_action": "",
            "preventative_action_datetime": None,
            "preventative_action": "",
            "report_closed_datetime": None,
            "action_required": REMAIN_ON_STUDY_MODIFIED,
            "missed_dose_conditions": "MISSED_GT_2D_INDUCTION_RX",
        }

    def test_missed_dose_conditions_applicable_if_remain_on_study_modified(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            {
                "action_required": REMAIN_ON_STUDY_MODIFIED,
                "missed_dose_conditions": NOT_APPLICABLE,
            },
        )
        form_validator = ProtocolDeviationViolationFormValidator(cleaned_data=cleaned_data)
        with self.assertRaises(ValidationError) as cm:
            form_validator.validate()
        self.assertIn("missed_dose_conditions", cm.exception.error_dict)
        self.assertEqual(
            {"missed_dose_conditions": ["This field is applicable."]},
            cm.exception.message_dict,
        )

    def test_missed_dose_conditions_with_remain_on_study_modified_ok(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            {
                "action_required": REMAIN_ON_STUDY_MODIFIED,
                "missed_dose_conditions": "MISSED_GT_2D_INDUCTION_RX",
            },
        )
        form_validator = ProtocolDeviationViolationFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got {e}")

    def test_missed_dose_conditions_not_applicable_if_not_remain_on_study_modified(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            {
                "action_required": "to_be_withdrawn",
                "missed_dose_conditions": "MISSED_GT_2D_INDUCTION_RX",
            },
        )
        form_validator = ProtocolDeviationViolationFormValidator(cleaned_data=cleaned_data)
        with self.assertRaises(ValidationError) as cm:
            form_validator.validate()
        self.assertIn("action_required_followup", cm.exception.error_dict)
        self.assertEqual(
            {"missed_dose_conditions": ["This field is not applicable."]},
            cm.exception.message_dict,
        )

    def test_missed_dose_conditions_na_if_not_remain_on_study_modified_ok(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            {
                "action_required": "to_be_withdrawn",
                "missed_dose_conditions": NOT_APPLICABLE,
            },
        )
        form_validator = ProtocolDeviationViolationFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got {e}")
