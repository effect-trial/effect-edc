from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from effect_form_validators.effect_subject import MedicalHistoryFormValidator

from ..models import MedicalHistory


class MedicalHistoryForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = MedicalHistoryFormValidator

    class Meta:
        model = MedicalHistory
        fields = "__all__"
