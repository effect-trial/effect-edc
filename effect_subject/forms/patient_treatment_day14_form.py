from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator
from edc_glucose.form_validators import GlucoseFormValidatorMixin

from ..models import PatientTreatmentDay14


class PatientTreatmentDay14FormValidator(GlucoseFormValidatorMixin, FormValidator):
    pass


class PatientTreatmentDay14Form(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = PatientTreatmentDay14FormValidator

    class Meta:
        model = PatientTreatmentDay14
        fields = "__all__"
