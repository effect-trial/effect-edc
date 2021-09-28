from edc_blood_results import BloodResultsFormValidatorMixin
from edc_form_validators.form_validator import FormValidator
from edc_lab_panel.panels import fbc_panel, lft_panel, rft_panel
from edc_reportable import BmiFormValidatorMixin


class BloodResultsFbcFormValidator(BloodResultsFormValidatorMixin, FormValidator):
    panel = fbc_panel


class BloodResultsLftFormValidator(BloodResultsFormValidatorMixin, FormValidator):
    panel = lft_panel


class BloodResultsRftFormValidator(
    BloodResultsFormValidatorMixin, BmiFormValidatorMixin, FormValidator
):
    panel = rft_panel

    def clean(self):
        super().clean()
        self.validate_bmi()


class BloodResultsLipidsFormValidator(BloodResultsFormValidatorMixin, FormValidator):
    panel = lipids_panel
