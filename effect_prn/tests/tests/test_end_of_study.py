from unittest.mock import patch

from django import forms
from django.test import TestCase, tag
from edc_adverse_event.form_validator_mixins import (
    RequiresDeathReportFormValidatorMixin,
)
from edc_constants.constants import DEAD, OTHER
from edc_form_validators import FormValidatorTestCaseMixin
from edc_ltfu.constants import LOST_TO_FOLLOWUP
from edc_ltfu.modelform_mixins import RequiresLtfuFormValidatorMixin
from edc_offstudy.constants import COMPLETED_FOLLOWUP
from edc_utils import get_utcnow, get_utcnow_as_date
from effect_form_validators.tests.mixins import TestCaseMixin

from effect_lists.models import OffstudyReasons
from effect_prn.form_validators import EndOfStudyFormValidator


@tag("eos")
class TestEndOfStudyFormValidation(FormValidatorTestCaseMixin, TestCaseMixin, TestCase):

    form_validator_default_form_cls = EndOfStudyFormValidator

    def mock_validate_ltfu(self):
        pass

    def mock_validate_death_report_if_deceased(self):
        pass

    def get_cleaned_data(self, **kwargs) -> dict:
        return {
            "subject_identifier": "123-456-1234-0",
            "offschedule_datetime": get_utcnow(),
            "offschedule_reason": OffstudyReasons.objects.get(name=COMPLETED_FOLLOWUP),
            "other_offschedule_reason": "",
            "ltfu_date": "",
            "death_date": "",
            "comment": "Some notes on eos",
        }

    def test_cleaned_data_ok(self):
        cleaned_data = self.get_cleaned_data()
        form_validator = EndOfStudyFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError as e:
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
        with self.assertRaises(forms.ValidationError) as cm:
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
        with self.assertRaises(forms.ValidationError) as cm:
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
        except forms.ValidationError as e:
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
        with self.assertRaises(forms.ValidationError) as cm:
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
        with self.assertRaises(forms.ValidationError) as cm:
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
        with self.assertRaises(forms.ValidationError) as cm:
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
        except forms.ValidationError as e:
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
        with self.assertRaises(forms.ValidationError) as cm:
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
        with self.assertRaises(forms.ValidationError) as cm:
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
        with self.assertRaises(forms.ValidationError) as cm:
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
        except forms.ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got {e}")
