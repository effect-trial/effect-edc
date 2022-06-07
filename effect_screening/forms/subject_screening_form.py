from typing import Any

from django import forms
from edc_form_validators import FormValidatorMixin
from edc_screening.modelform_mixins import AlreadyConsentedFormMixin
from effect_form_validators.effect_screening import (
    SubjectScreeningFormValidator as Base,
)

from ..models import SubjectScreening


class SubjectScreeningFormValidator(Base):
    pass


class SubjectScreeningForm(AlreadyConsentedFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = SubjectScreeningFormValidator

    screening_identifier = forms.CharField(
        label="Screening Identifier",
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )

    subject_identifier = forms.CharField(
        label="Subject identifier",
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )

    def clean(self: Any) -> dict:
        cleaned_data = super().clean()
        return cleaned_data

    class Meta:
        model = SubjectScreening
        fields = "__all__"
        labels = {
            "hiv_dx_ago": "If YES, how long ago did the patient test HIV sero-positive?",
            "hiv_dx_date": "If YES, date patient tested HIV sero-positive",
        }
