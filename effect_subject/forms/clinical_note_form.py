from django import forms
from edc_constants.constants import YES
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator
from edc_glucose.form_validators import GlucoseFormValidatorMixin

from ..models import ClinicalNote


class ClinicalNoteFormValidator(GlucoseFormValidatorMixin, FormValidator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.has_comment = self.cleaned_data.get("has_comment")
        self.comments = self.cleaned_data.get("comments")

    def clean(self):
        super().clean()

        # self.applicable_if(YES, field="has_comment", field_applicable="comments")
        self.required_if(YES, field="has_comment", field_required="comments")


class ClinicalNoteForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = ClinicalNoteFormValidator

    class Meta:
        model = ClinicalNote
        fields = "__all__"
