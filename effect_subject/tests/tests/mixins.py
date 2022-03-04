from django.test import TestCase
from edc_constants.constants import NO, NOT_APPLICABLE, YES
from edc_visit_schedule.constants import DAY1

from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin
from effect_visit_schedule.constants import DAY14


class ReportingFieldsetBaselineTestCaseMixin(EffectTestCaseMixin, TestCase):
    default_cleaned_data = None

    def test_baseline_cleaned_data_valid(self):
        """Test that the test data we're working with is valid."""
        cleaned_data = self.default_cleaned_data(visit_code=DAY1)
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_reportable_as_ae_not_applicable_at_baseline(self):
        cleaned_data = self.default_cleaned_data(visit_code=DAY1)
        for response in [YES, NO]:
            with self.subTest(reportable_as_ae=response):
                cleaned_data.update({"reportable_as_ae": response})
                self.assertFormValidatorError(
                    field="reportable_as_ae",
                    expected_msg="This field is not applicable at baseline.",
                    form_validator=self.validate_form_validator(cleaned_data),
                )

    def test_patient_admitted_not_applicable_at_baseline(self):
        cleaned_data = self.default_cleaned_data(visit_code=DAY1)
        for response in [YES, NO]:
            with self.subTest(patient_admitted=response):
                cleaned_data.update({"patient_admitted": response})
                self.assertFormValidatorError(
                    field="patient_admitted",
                    expected_msg="This field is not applicable at baseline.",
                    form_validator=self.validate_form_validator(cleaned_data),
                )


class ReportingFieldsetDay14TestCaseMixin(EffectTestCaseMixin, TestCase):
    default_cleaned_data = None

    def test_d14_cleaned_data_valid(self):
        """Test that the test data we're working with is valid."""
        cleaned_data = self.default_cleaned_data(visit_code=DAY14)
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_reportable_as_ae_applicable_at_d14(self):
        cleaned_data = self.default_cleaned_data(visit_code=DAY14)
        cleaned_data.update({"reportable_as_ae": NOT_APPLICABLE})
        self.assertFormValidatorError(
            field="reportable_as_ae",
            expected_msg="This field is applicable.",
            form_validator=self.validate_form_validator(cleaned_data),
        )
        for response in [YES, NO]:
            with self.subTest(reportable_as_ae=response):
                cleaned_data.update({"reportable_as_ae": response})
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(cleaned_data)
                )

    def test_patient_admitted_applicable_at_d14(self):
        cleaned_data = self.default_cleaned_data(visit_code=DAY14)
        cleaned_data.update({"patient_admitted": NOT_APPLICABLE})
        self.assertFormValidatorError(
            field="patient_admitted",
            expected_msg="This field is applicable.",
            form_validator=self.validate_form_validator(cleaned_data),
        )
        for response in [YES, NO]:
            with self.subTest(patient_admitted=response):
                cleaned_data.update({"patient_admitted": response})
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(cleaned_data)
                )
