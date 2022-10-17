from django import forms
from edc_action_item.forms import ActionItemCrfFormMixin
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_lab_results.form_validator_mixins import BloodResultsFormValidatorMixin

from effect_labs.panels import urinalysis_panel

from ...models import Urinalysis


class UrinalysisFormValidator(BloodResultsFormValidatorMixin, CrfFormValidator):
    panel = urinalysis_panel


class UrinalysisForm(ActionItemCrfFormMixin, CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = UrinalysisFormValidator

    class Meta(ActionItemCrfFormMixin.Meta):
        model = Urinalysis
        fields = "__all__"
