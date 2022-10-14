from django import forms
from edc_action_item.forms import ActionItemCrfFormMixin
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_lab_results.form_validator_mixins import BloodResultsFormValidatorMixin

from effect_labs.panels import fbc_panel

from ...models import BloodResultsFbc


class BloodResultsFbcFormValidator(BloodResultsFormValidatorMixin, CrfFormValidator):
    panel = fbc_panel


class BloodResultsFbcForm(ActionItemCrfFormMixin, CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = BloodResultsFbcFormValidator

    class Meta:
        model = BloodResultsFbc
        fields = "__all__"
