from django import forms
from edc_constants.constants import YES
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator

from ..models import ClinicalNote


class ClinicalNoteFormValidator(FormValidator):
    def clean(self):
        self.required_if(YES, field="has_comment", field_required="comments")


class ClinicalNoteForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = ClinicalNoteFormValidator

    class Meta:
        model = ClinicalNote
        fields = "__all__"
