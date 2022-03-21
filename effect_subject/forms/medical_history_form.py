from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator

from ..models import MedicalHistory


class MedicalHistoryFormValidator(FormValidator):
    pass


class MedicalHistoryForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = MedicalHistoryFormValidator

    class Meta:
        model = MedicalHistory
        fields = "__all__"
