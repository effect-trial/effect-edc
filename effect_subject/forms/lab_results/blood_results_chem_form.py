from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import FormValidator
from edc_lab_results.form_validator_mixins import BloodResultsFormValidatorMixin

from ...models import BloodResultsChem


class BloodResultsChemFormValidator(BloodResultsFormValidatorMixin, FormValidator):
    panel = BloodResultsChem.lab_panel


class BloodResultsChemForm(ActionItemFormMixin, CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = BloodResultsChemFormValidator

    class Meta:
        model = BloodResultsChem
        fields = "__all__"
