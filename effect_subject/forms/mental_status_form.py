from django import forms
from edc_constants.constants import YES
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator
from edc_visit_schedule.utils import is_baseline

from ..models import MentalStatus
from .mixins import ReportingFieldsetFormValidatorMixin


class MentalStatusFormValidator(ReportingFieldsetFormValidatorMixin, FormValidator):
    def clean(self) -> None:

        self.validate_baseline_exclusions()

        self.validate_reporting_fieldset_na_baseline()

        self.validate_reporting_fieldset_applicable_if_not_baseline()

    def validate_baseline_exclusions(self):
        if is_baseline(self.cleaned_data.get("subject_visit")):
            if self.cleaned_data.get("recent_seizure") == YES:
                raise forms.ValidationError(
                    {
                        "recent_seizure": (
                            "Invalid. Cannot have had a recent seizure at baseline"
                        )
                    }
                )
            elif (
                self.cleaned_data.get("glasgow_coma_score")
                and self.cleaned_data.get("glasgow_coma_score") < 15
            ):
                raise forms.ValidationError(
                    {
                        "glasgow_coma_score": "Invalid. GCS cannot be less than 15 at baseline"
                    }
                )


class MentalStatusForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = MentalStatusFormValidator

    class Meta:
        model = MentalStatus
        fields = "__all__"
