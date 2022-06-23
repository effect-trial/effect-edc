from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from effect_form_validators.effect_subject import PatientHistoryFormValidator

from ..models import PatientHistory


class PatientHistoryForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = PatientHistoryFormValidator

    class Meta:
        model = PatientHistory
        fields = "__all__"
