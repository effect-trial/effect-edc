from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_blood_results import BloodResultsFormValidatorMixin
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import FormValidator
from edc_lab_panel.panels import hba1c_panel

from ...models import BloodResultsHba1c


class BloodResultsHba1cFormValidator(BloodResultsFormValidatorMixin, FormValidator):
    panels = hba1c_panel


class BloodResultsHba1cForm(ActionItemFormMixin, CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = BloodResultsHba1cFormValidator

    class Meta:
        model = BloodResultsHba1c
        fields = "__all__"
