from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from effect_form_validators.effect_subject import ClinicalNoteFormValidator

from ..models import ClinicalNote


class ClinicalNoteForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = ClinicalNoteFormValidator

    class Meta:
        model = ClinicalNote
        fields = "__all__"
