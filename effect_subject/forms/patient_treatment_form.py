from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from effect_form_validators.effect_subject import PatientTreatmentFormValidator

from ..models import PatientTreatment


class PatientTreatmentForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = PatientTreatmentFormValidator

    class Meta:
        model = PatientTreatment
        fields = "__all__"
