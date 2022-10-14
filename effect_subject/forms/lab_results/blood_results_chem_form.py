from django import forms
from django.utils.safestring import mark_safe
from edc_action_item.forms import ActionItemCrfFormMixin
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import INVALID_ERROR
from edc_lab_results.form_validator_mixins import BloodResultsFormValidatorMixin

from ...models import BloodResultsChem
from ...utils import get_weight_in_kgs


class BloodResultsChemFormValidator(BloodResultsFormValidatorMixin, CrfFormValidator):
    panel = BloodResultsChem.lab_panel

    def clean(self) -> None:
        if self.cleaned_data.get("creatinine_value") and not get_weight_in_kgs(
            subject_visit=self.related_visit
        ):
            self.raise_validation_error(
                "Participant weight not found. Please complete the Vital Signs CRF first.",
                INVALID_ERROR,
            )

        super().clean()


class BloodResultsChemForm(ActionItemCrfFormMixin, CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = BloodResultsChemFormValidator

    class Meta(ActionItemCrfFormMixin.Meta):
        model = BloodResultsChem
        fields = "__all__"
        help_texts = {
            "action_identifier": "(read-only)",
            "egfr_value": mark_safe(  # nosec B308
                "Calculated using Cockcroft-Gault equation. "
                "See https://www.mdcalc.com/creatinine-clearance-cockcroft-gault-equation"
            ),
        }
