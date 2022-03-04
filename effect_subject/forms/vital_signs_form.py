from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator

from ..models import VitalSigns


class VitalSignsFormValidator(FormValidator):
    def clean(self) -> None:
        self.required_if_true(True, field_required="sys_blood_pressure")
        self.required_if_true(True, field_required="dia_blood_pressure")


class VitalSignsForm(CrfModelFormMixin, ActionItemFormMixin, forms.ModelForm):
    form_validator_cls = VitalSignsFormValidator

    class Meta:
        model = VitalSigns
        fields = "__all__"
