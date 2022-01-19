from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator
from edc_glucose.form_validators import GlucoseFormValidatorMixin

from ..models import VitalSigns


class VitalSignsFormValidator(GlucoseFormValidatorMixin, FormValidator):
    pass


class VitalSignsForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = VitalSignsFormValidator

    class Meta:
        model = VitalSigns
        fields = "__all__"
