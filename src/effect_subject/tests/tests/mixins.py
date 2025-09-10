from typing import Any, Optional

from edc_constants.constants import NO, NOT_APPLICABLE, YES

from effect_visit_schedule.constants import DAY14


class ReportingFieldsetDay14TestCaseMixin:
    def default_cleaned_data(self, visit_code: Optional[str] = None) -> dict:
        return {}

    def test_d14_cleaned_data_valid(self: Any):
        """Test that the test data we're working with is valid."""
        cleaned_data = self.default_cleaned_data(visit_code=DAY14)
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_reportable_as_ae_applicable_at_d14(self: Any):
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

    def test_patient_admitted_applicable_at_d14(self: Any):
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
