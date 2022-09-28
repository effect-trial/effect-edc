from unittest.mock import patch

from django.forms import ValidationError
from django.test import TestCase, tag
from edc_adverse_event.form_validator_mixins import (
    RequiresDeathReportFormValidatorMixin,
)
from edc_consent.constants import CONSENT_WITHDRAWAL
from edc_constants.constants import DEAD, NO, NOT_APPLICABLE, OTHER, YES
from edc_form_validators import FormValidatorTestCaseMixin
from edc_ltfu.constants import LOST_TO_FOLLOWUP
from edc_ltfu.modelform_mixins import RequiresLtfuFormValidatorMixin
from edc_offstudy.constants import COMPLETED_FOLLOWUP, INVALID_ENROLMENT, LATE_EXCLUSION
from edc_transfer.constants import TRANSFERRED
from edc_utils import get_utcnow, get_utcnow_as_date

from effect_lists.models import LateExclusionCriteria, OffstudyReasons
from effect_prn.forms.end_of_study_form import EndOfStudyFormValidator


@tag("eos")
class TestEndOfStudyFormValidation(FormValidatorTestCaseMixin, TestCase):

    form_validator_cls = EndOfStudyFormValidator

    def mock_validate_ltfu(self):
        pass

    def mock_validate_death_report_if_deceased(self):
        pass

    @staticmethod
    def get_cleaned_data() -> dict:
        return {
            "subject_identifier": "123-456-1234-0",
            "offschedule_datetime": get_utcnow(),
            "offschedule_reason": OffstudyReasons.objects.get(name=COMPLETED_FOLLOWUP),
            "other_offschedule_reason": "",
            "ltfu_date": "",
            "death_date": "",
            "consent_withdrawal_reason": "",
            "late_exclusion_reasons": LateExclusionCriteria.objects.none(),
            "transferred_consent": NOT_APPLICABLE,
            "invalid_enrol_reason": "",
            "comment": "Some notes on eos",
        }

    def test_cleaned_data_ok(self):
        cleaned_data = self.get_cleaned_data()
        form_validator = EndOfStudyFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got {e}")

    def test_other_offschedule_reason_required_if_offschedule_reason_other(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            {
                "offschedule_reason": OffstudyReasons.objects.get(name=OTHER),
                "other_offschedule_reason": "",
            }
        )
        form_validator = EndOfStudyFormValidator(cleaned_data=cleaned_data)
        with self.assertRaises(ValidationError) as cm:
            form_validator.validate()
        self.assertIn("other_offschedule_reason", cm.exception.error_dict)
        self.assertEqual(
            {"other_offschedule_reason": ["This field is required."]},
            cm.exception.message_dict,
        )

    def test_other_offschedule_reason_not_required_if_offschedule_reason_not_other(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            {
                "offschedule_reason": OffstudyReasons.objects.get(name=COMPLETED_FOLLOWUP),
                "other_offschedule_reason": "Some other reason",
            }
        )
        form_validator = EndOfStudyFormValidator(cleaned_data=cleaned_data)
        with self.assertRaises(ValidationError) as cm:
            form_validator.validate()
        self.assertIn("other_offschedule_reason", cm.exception.error_dict)
        self.assertEqual(
            {"other_offschedule_reason": ["This field is not required."]},
            cm.exception.message_dict,
        )

    def test_other_offschedule_reason_with_offschedule_reason_other_ok(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            {
                "offschedule_reason": OffstudyReasons.objects.get(name=OTHER),
                "other_offschedule_reason": "Some other reason",
            }
        )
        form_validator = EndOfStudyFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got {e}")

    def test_offschedule_reason_dead_with_no_death_form_raises(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            {
                "offschedule_reason": OffstudyReasons.objects.get(name=DEAD),
                "death_date": get_utcnow_as_date(),
            }
        )
        form_validator = EndOfStudyFormValidator(cleaned_data=cleaned_data)
        with self.assertRaises(ValidationError) as cm:
            form_validator.validate()
        self.assertIn("offschedule_reason", cm.exception.error_dict)
        self.assertEqual(
            {
                "offschedule_reason": [
                    "Patient is deceased, please complete death report form first."
                ]
            },
            cm.exception.message_dict,
        )

    @patch.object(
        RequiresDeathReportFormValidatorMixin,
        "validate_death_report_if_deceased",
        mock_validate_death_report_if_deceased,
    )
    def test_death_date_required_if_offschedule_reason_dead(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            {
                "offschedule_reason": OffstudyReasons.objects.get(name=DEAD),
                "death_date": None,
            }
        )
        form_validator = EndOfStudyFormValidator(cleaned_data=cleaned_data)
        with self.assertRaises(ValidationError) as cm:
            form_validator.validate()
        self.assertIn("death_date", cm.exception.error_dict)
        self.assertEqual(
            {"death_date": ["This field is required."]},
            cm.exception.message_dict,
        )

    def test_death_date_not_required_if_offschedule_reason_not_dead(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            {
                "offschedule_reason": OffstudyReasons.objects.get(name=COMPLETED_FOLLOWUP),
                "death_date": get_utcnow_as_date(),
            }
        )
        form_validator = EndOfStudyFormValidator(cleaned_data=cleaned_data)
        with self.assertRaises(ValidationError) as cm:
            form_validator.validate()
        self.assertIn("death_date", cm.exception.error_dict)
        self.assertEqual(
            {"death_date": ["This field is not required."]},
            cm.exception.message_dict,
        )

    @patch.object(
        RequiresDeathReportFormValidatorMixin,
        "validate_death_report_if_deceased",
        mock_validate_death_report_if_deceased,
    )
    def test_death_date_with_offschedule_reason_dead_ok(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            {
                "offschedule_reason": OffstudyReasons.objects.get(name=DEAD),
                "death_date": get_utcnow_as_date(),
            }
        )
        form_validator = EndOfStudyFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got {e}")

    def test_offschedule_reason_ltfu_with_no_ltfu_form_raises(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            {
                "offschedule_reason": OffstudyReasons.objects.get(name=LOST_TO_FOLLOWUP),
                "ltfu_date": get_utcnow_as_date(),
            }
        )
        form_validator = EndOfStudyFormValidator(cleaned_data=cleaned_data)
        with self.assertRaises(ValidationError) as cm:
            form_validator.validate()
        self.assertIn("offschedule_reason", cm.exception.error_dict)
        self.assertEqual(
            {
                "offschedule_reason": [
                    "Patient is lost to followup, please complete "
                    "`Loss to Follow Up` form first."
                ]
            },
            cm.exception.message_dict,
        )

    @patch.object(RequiresLtfuFormValidatorMixin, "validate_ltfu", mock_validate_ltfu)
    def test_ltfu_date_required_if_offschedule_reason_ltfu(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            {
                "offschedule_reason": OffstudyReasons.objects.get(name=LOST_TO_FOLLOWUP),
                "ltfu_date": None,
            }
        )
        form_validator = EndOfStudyFormValidator(cleaned_data=cleaned_data)
        with self.assertRaises(ValidationError) as cm:
            form_validator.validate()
        self.assertIn("ltfu_date", cm.exception.error_dict)
        self.assertEqual(
            {"ltfu_date": ["This field is required."]},
            cm.exception.message_dict,
        )

    def test_ltfu_date_not_required_if_offschedule_reason_not_ltfu(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            {
                "offschedule_reason": OffstudyReasons.objects.get(name=COMPLETED_FOLLOWUP),
                "ltfu_date": get_utcnow_as_date(),
            }
        )
        form_validator = EndOfStudyFormValidator(cleaned_data=cleaned_data)
        with self.assertRaises(ValidationError) as cm:
            form_validator.validate()
        self.assertIn("ltfu_date", cm.exception.error_dict)
        self.assertEqual(
            {"ltfu_date": ["This field is not required."]},
            cm.exception.message_dict,
        )

    @patch.object(RequiresLtfuFormValidatorMixin, "validate_ltfu", mock_validate_ltfu)
    def test_ltfu_date_with_offschedule_reason_ltfu_ok(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            {
                "offschedule_reason": OffstudyReasons.objects.get(name=LOST_TO_FOLLOWUP),
                "ltfu_date": get_utcnow_as_date(),
            }
        )
        form_validator = EndOfStudyFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got {e}")

    def test_consent_withdrawal_reason_required_if_offschedule_reason_consent_withdrawal(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            {
                "offschedule_reason": OffstudyReasons.objects.get(name=CONSENT_WITHDRAWAL),
                "consent_withdrawal_reason": "",
            }
        )
        form_validator = EndOfStudyFormValidator(cleaned_data=cleaned_data)
        with self.assertRaises(ValidationError) as cm:
            form_validator.validate()
        self.assertIn("consent_withdrawal_reason", cm.exception.error_dict)
        self.assertEqual(
            {"consent_withdrawal_reason": ["This field is required."]},
            cm.exception.message_dict,
        )

    def test_consent_withdrawal_reason_not_required_if_offschedule_reason_not_consent_withdrawal(  # noqa: E501
        self,
    ):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            {
                "offschedule_reason": OffstudyReasons.objects.get(name=COMPLETED_FOLLOWUP),
                "consent_withdrawal_reason": "Some reason...",
            }
        )
        form_validator = EndOfStudyFormValidator(cleaned_data=cleaned_data)
        with self.assertRaises(ValidationError) as cm:
            form_validator.validate()
        self.assertIn("consent_withdrawal_reason", cm.exception.error_dict)
        self.assertEqual(
            {"consent_withdrawal_reason": ["This field is not required."]},
            cm.exception.message_dict,
        )

    def test_consent_withdrawal_reason_with_offschedule_reason_consent_withdrawal_ok(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            {
                "offschedule_reason": OffstudyReasons.objects.get(name=CONSENT_WITHDRAWAL),
                "consent_withdrawal_reason": "Reason for withdrawal",
            }
        )
        form_validator = EndOfStudyFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got {e}")

    def test_offschedule_reason_not_selected_does_not_raise_attribute_error(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update({"offschedule_reason": OffstudyReasons.objects.none()}),
        form_validator = EndOfStudyFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except AttributeError as e:
            self.fail(f"ValidationError unexpectedly raised. Got {e}")

    def test_late_exclusion_reasons_required_if_offschedule_reason_late_exclusion(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            {
                "offschedule_reason": OffstudyReasons.objects.get(name=LATE_EXCLUSION),
                "late_exclusion_reasons": LateExclusionCriteria.objects.none(),
            }
        )
        form_validator = EndOfStudyFormValidator(cleaned_data=cleaned_data)
        with self.assertRaises(ValidationError) as cm:
            form_validator.validate()
        self.assertIn("late_exclusion_reasons", cm.exception.error_dict)
        self.assertEqual(
            {"late_exclusion_reasons": ["This field is required"]},
            cm.exception.message_dict,
        )

    def test_late_exclusion_reasons_not_required_if_offschedule_reason_not_late_exclusion(
        self,
    ):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            {
                "offschedule_reason": OffstudyReasons.objects.get(name=COMPLETED_FOLLOWUP),
                "late_exclusion_reasons": LateExclusionCriteria.objects.filter(
                    name="cm_evidence_screening_csf"
                ),
            }
        )
        form_validator = EndOfStudyFormValidator(cleaned_data=cleaned_data)
        with self.assertRaises(ValidationError) as cm:
            form_validator.validate()
        self.assertIn("late_exclusion_reasons", cm.exception.error_dict)
        self.assertEqual(
            {"late_exclusion_reasons": ["This field is not required"]},
            cm.exception.message_dict,
        )

    def test_late_exclusion_reasons_with_offschedule_reason_late_exclusion_ok(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            {
                "offschedule_reason": OffstudyReasons.objects.get(name=LATE_EXCLUSION),
                "late_exclusion_reasons": LateExclusionCriteria.objects.filter(
                    name="cm_evidence_screening_csf"
                ),
            }
        )
        form_validator = EndOfStudyFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got {e}")

    def test_multiple_late_exclusion_reasons__ok(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            {
                "offschedule_reason": OffstudyReasons.objects.get(name=LATE_EXCLUSION),
                "late_exclusion_reasons": LateExclusionCriteria.objects.all(),
            }
        )
        form_validator = EndOfStudyFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got {e}")

    def test_transferred_consent_applicable_if_offschedule_reason_transferred(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            {
                "offschedule_reason": OffstudyReasons.objects.get(name=TRANSFERRED),
                "transferred_consent": NOT_APPLICABLE,
            }
        )
        form_validator = EndOfStudyFormValidator(cleaned_data=cleaned_data)
        with self.assertRaises(ValidationError) as cm:
            form_validator.validate()
        self.assertIn("transferred_consent", cm.exception.error_dict)
        self.assertEqual(
            {"transferred_consent": ["This field is applicable."]},
            cm.exception.message_dict,
        )

    def test_transferred_consent_not_applicable_if_offschedule_reason_not_transferred(self):
        for answer in [YES, NO]:
            with self.subTest(transferred_consent_answer=answer):
                cleaned_data = self.get_cleaned_data()
                cleaned_data.update(
                    {
                        "offschedule_reason": OffstudyReasons.objects.get(
                            name=COMPLETED_FOLLOWUP
                        ),
                        "transferred_consent": answer,
                    }
                )
                form_validator = EndOfStudyFormValidator(cleaned_data=cleaned_data)
                with self.assertRaises(ValidationError) as cm:
                    form_validator.validate()
                self.assertIn("transferred_consent", cm.exception.error_dict)
                self.assertEqual(
                    {"transferred_consent": ["This field is not applicable."]},
                    cm.exception.message_dict,
                )

    def test_transferred_consent_answers_with_offschedule_reason_transferred_ok(self):
        for answer in [YES, NO]:
            with self.subTest(transferred_consent_answer=answer):
                cleaned_data = self.get_cleaned_data()
                cleaned_data.update(
                    {
                        "offschedule_reason": OffstudyReasons.objects.get(name=TRANSFERRED),
                        "transferred_consent": answer,
                    }
                )
                form_validator = EndOfStudyFormValidator(cleaned_data=cleaned_data)
                try:
                    form_validator.validate()
                except ValidationError as e:
                    self.fail(f"ValidationError unexpectedly raised. Got {e}")

    def test_invalid_enrol_reason_required_if_offschedule_reason_invalid_enrolment(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            {
                "offschedule_reason": OffstudyReasons.objects.get(name=INVALID_ENROLMENT),
                "invalid_enrol_reason": "",
            }
        )
        form_validator = EndOfStudyFormValidator(cleaned_data=cleaned_data)
        with self.assertRaises(ValidationError) as cm:
            form_validator.validate()
        self.assertIn("invalid_enrol_reason", cm.exception.error_dict)
        self.assertEqual(
            {"invalid_enrol_reason": ["This field is required."]},
            cm.exception.message_dict,
        )

    def test_invalid_enrol_reason_not_required_if_offschedule_reason_not_invalid_enrolment(
        self,
    ):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            {
                "offschedule_reason": OffstudyReasons.objects.get(name=COMPLETED_FOLLOWUP),
                "invalid_enrol_reason": "Some reason...",
            }
        )
        form_validator = EndOfStudyFormValidator(cleaned_data=cleaned_data)
        with self.assertRaises(ValidationError) as cm:
            form_validator.validate()
        self.assertIn("invalid_enrol_reason", cm.exception.error_dict)
        self.assertEqual(
            {"invalid_enrol_reason": ["This field is not required."]},
            cm.exception.message_dict,
        )

    def test_invalid_enrol_reason_with_offschedule_reason_invalid_enrolment_ok(self):
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            {
                "offschedule_reason": OffstudyReasons.objects.get(name=INVALID_ENROLMENT),
                "invalid_enrol_reason": "Details of invalid enrolment",
            }
        )
        form_validator = EndOfStudyFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got {e}")
