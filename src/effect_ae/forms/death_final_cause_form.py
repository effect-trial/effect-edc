from clinicedc_constants import OTHER
from django import forms
from edc_form_validators import FormValidator, FormValidatorMixin

from ..models import DeathFinalCause


class DeathFinalCauseFormValidator(FormValidator):
    def clean(self) -> None:
        self.required_if(
            OTHER,
            field="final_cause_of_death",
            field_required="final_cause_of_death_other",
        )


class DeathFinalCauseForm(FormValidatorMixin, forms.ModelForm):
    """Form for reconciling the final cause of death post-closure."""

    form_validator_cls = DeathFinalCauseFormValidator

    class Meta:
        model = DeathFinalCause
        fields = "__all__"
