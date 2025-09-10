from django import forms
from edc_form_validators import FormValidatorMixin
from edc_screening.modelform_mixins import AlreadyConsentedFormMixin
from edc_sites.modelform_mixins import SiteModelFormMixin
from effect_form_validators.effect_screening import SubjectScreeningFormValidator

from ..models import SubjectScreening


class SubjectScreeningForm(
    AlreadyConsentedFormMixin, SiteModelFormMixin, FormValidatorMixin, forms.ModelForm
):
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

    safe_save_id = forms.UUIDField(
        label="Safe save ID",
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )

    class Meta:
        model = SubjectScreening
        labels = {
            "gender": "Sex",
            "unsuitable_agreed": (
                "Does the study clinician agree that the patient is not "
                "suitable for the study?"
            ),
        }
        exclude = [
            "eligibility_datetime",
            "real_eligibility_datetime",
            "reasons_ineligible",
        ]
