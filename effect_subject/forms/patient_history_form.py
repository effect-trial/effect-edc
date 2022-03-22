from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator

from ..models import PatientHistory


class PatientHistoryFormValidator(FormValidator):
    pass


class PatientHistoryForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = PatientHistoryFormValidator

    class Meta:
        model = PatientHistory
        fields = "__all__"
