from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator
from edc_glucose.form_validators import GlucoseFormValidatorMixin

from ..models import ClinicalNote


class ClinicalNoteFormValidator(GlucoseFormValidatorMixin, FormValidator):
    pass


class ClinicalNoteForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = ClinicalNoteFormValidator

    class Meta:
        model = ClinicalNote
        fields = "__all__"
