from django import forms
from edc_constants.constants import DEAD, YES
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator
from edc_glucose.form_validators import GlucoseFormValidatorMixin

from ..constants import IN_PERSON, PATIENT, TELEPHONE
from ..models import Followup


class FollowupFormValidator(GlucoseFormValidatorMixin, FormValidator):
    def clean(self):
        super().clean()

        self.applicable_if(
            TELEPHONE, field="assessment_type", field_applicable="info_source"
        )
        self.validate_other_specify(field="info_source")
        self.validate_survival_status()
        self.validate_adherence_counselling()

    def validate_survival_status(self):
        if (
            self.cleaned_data.get("survival_status") == DEAD
            and self.cleaned_data.get("assessment_type") == IN_PERSON
        ):
            raise forms.ValidationError(
                {
                    "survival_status": (
                        "Invalid: Unexpected survival status 'Deceased' if "
                        "'In person' visit"
                    )
                }
            )
        elif (
            self.cleaned_data.get("survival_status") == DEAD
            and self.cleaned_data.get("assessment_type") == TELEPHONE
            and self.cleaned_data.get("info_source") == PATIENT
        ):
            raise forms.ValidationError(
                {
                    "survival_status": (
                        "Invalid: Unexpected survival status 'Deceased' if "
                        "'Telephone' visit with 'Patient'"
                    )
                }
            )

    def validate_adherence_counselling(self):
        if (
            self.cleaned_data.get("adherence_counselling") == YES
            and self.cleaned_data.get("survival_status") == DEAD
        ):
            raise forms.ValidationError(
                {
                    "adherence_counselling": (
                        "Invalid: Adherence counselling not expected if "
                        "survival status is 'Deceased'"
                    )
                }
            )


class FollowupForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = FollowupFormValidator

    class Meta:
        model = Followup
        fields = "__all__"
