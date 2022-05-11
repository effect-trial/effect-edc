from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import FormValidator
from edc_lab_results.form_validator_mixins import BloodResultsFormValidatorMixin

from effect_labs.panels import urinalysis_panel

from ...models import Urinalysis


class UrinalysisFormValidator(BloodResultsFormValidatorMixin, FormValidator):
    panel = urinalysis_panel


class UrinalysisForm(ActionItemFormMixin, CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = UrinalysisFormValidator

    class Meta:
        model = Urinalysis
        fields = "__all__"
