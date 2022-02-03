from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator
from edc_glucose.form_validators import GlucoseFormValidatorMixin

from ..models import VitalSigns


class VitalSignsFormValidator(GlucoseFormValidatorMixin, FormValidator):
    def clean(self) -> None:
        super().clean()

        self.required_if_true(True, field_required="sys_blood_pressure")
        self.required_if_true(True, field_required="dia_blood_pressure")


class VitalSignsForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = VitalSignsFormValidator

    class Meta:
        model = VitalSigns
        fields = "__all__"
