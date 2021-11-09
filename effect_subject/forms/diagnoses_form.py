from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator
from edc_glucose.form_validators import GlucoseFormValidatorMixin

from ..models import Diagnoses


class DiagnosesFormValidator(GlucoseFormValidatorMixin, FormValidator):
    pass


class DiagnosesForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = DiagnosesFormValidator

    class Meta:
        model = Diagnoses
        fields = "__all__"
