from django import forms
from edc_constants.constants import NO, NOT_APPLICABLE, OTHER, YES
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator

from ..models import Diagnoses
from .mixins import ReportingFieldsetFormValidatorMixin


class DiagnosesFormValidator(ReportingFieldsetFormValidatorMixin, FormValidator):
    def clean(self) -> None:

        self.validate_diagnoses()

        # TODO: validate reporting na if no dx
        self.validate_reporting_fieldset_na_baseline()

    def validate_diagnoses(self):
        if self.cleaned_data.get("has_diagnoses") == NO:
            self.m2m_selection_expected(
                NOT_APPLICABLE,
                m2m_field="diagnoses",
                error_msg="Expected N/A only if NO significant diagnoses to report.",
            )
        elif self.cleaned_data.get("has_diagnoses") == YES:
            self.m2m_selections_not_expected(
                NOT_APPLICABLE,
                m2m_field="diagnoses",
                error_msg=(
                    "Invalid selection. "
                    "Cannot be N/A if there are significant diagnoses to report."
                ),
            )
        self.m2m_other_specify(
            OTHER, m2m_field="diagnoses", field_other="diagnoses_other"
        )


class DiagnosesForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = DiagnosesFormValidator

    class Meta:
        model = Diagnoses
        fields = "__all__"
