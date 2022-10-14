from django import forms
from edc_action_item.forms import ActionItemCrfFormMixin
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_lab_results.form_validator_mixins import BloodResultsFormValidatorMixin

from ...models import BloodResultsChem


class BloodResultsChemFormValidator(BloodResultsFormValidatorMixin, CrfFormValidator):
    panel = BloodResultsChem.lab_panel


class BloodResultsChemForm(ActionItemCrfFormMixin, CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = BloodResultsChemFormValidator

    class Meta:
        model = BloodResultsChem
        fields = "__all__"
