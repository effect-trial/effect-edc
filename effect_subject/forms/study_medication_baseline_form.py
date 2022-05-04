from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from effect_form_validators.effect_subject import StudyMedicationBaselineFormValidator

from ..models import StudyMedicationBaseline


class StudyMedicationBaselineForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = StudyMedicationBaselineFormValidator

    class Meta:
        model = StudyMedicationBaseline
        fields = "__all__"
