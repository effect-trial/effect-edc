from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin

from ..models import MedicalHistory


class MedicalHistoryForm(CrfModelFormMixin, forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = "__all__"
