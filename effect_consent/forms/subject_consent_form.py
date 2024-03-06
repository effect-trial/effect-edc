from django import forms
from django.utils.html import format_html
from edc_consent.modelform_mixins import ConsentModelFormMixin
from edc_constants.constants import NO, YES
from edc_form_validators import FormValidatorMixin
from edc_sites.forms import SiteModelFormMixin
from effect_form_validators.effect_consent import SubjectConsentFormValidator

from ..models import SubjectConsent


class SubjectConsentForm(
    SiteModelFormMixin, FormValidatorMixin, ConsentModelFormMixin, forms.ModelForm
):
    form_validator_cls = SubjectConsentFormValidator

    screening_identifier = forms.CharField(
        label="Screening identifier",
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )

    def validate_guardian_and_dob(self):
        return None

    # def validate_identity_with_unique_fields(self):
    #     return None

    def validate_is_literate_and_witness(self) -> None:
        self.clean_is_literate_is_able_and_witness()

    def clean_is_literate_is_able_and_witness(self) -> None:
        cleaned_data = self.cleaned_data
        is_literate = cleaned_data.get("is_literate")
        is_able = cleaned_data.get("is_able")
        witness_name = cleaned_data.get("witness_name")
        if (is_literate == NO or is_able == NO) and not witness_name:
            raise forms.ValidationError(
                {
                    "witness_name": "Provide a name of a witness on this form and "
                    "ensure paper consent is signed."
                }
            )
        if is_literate == YES and is_able == YES and witness_name:
            raise forms.ValidationError({"witness_name": "This field is not required"})

    class Meta:
        model = SubjectConsent
        fields = "__all__"
        labels = {"gender": "Sex"}
        help_texts = {
            "identity": (
                "Use Country ID Number, Passport number, driver's license "
                "number or Country ID receipt number"
            ),
            "witness_name": format_html(
                "Required only if participant is illiterate or unable to provide consent.<br>"
                "Format is 'LASTNAME, FIRSTNAME'. "
                "All uppercase separated by a comma."
            ),
        }
