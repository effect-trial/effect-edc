from django import forms
from edc_constants.constants import NO, NOT_APPLICABLE, OTHER, YES
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator
from edc_visit_schedule.utils import is_baseline

from ..models import Diagnoses
from .mixins import ReportingFieldsetFormValidatorMixin


class DiagnosesFormValidator(ReportingFieldsetFormValidatorMixin, FormValidator):
    def clean(self) -> None:

        self.validate_diagnoses()

        self.validate_reporting_fieldset()

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

    def validate_reporting_fieldset(self):
        # TODO: Diagnoses CRF not completed at baseline visit, pull out baseline validation
        self.validate_reporting_fieldset_na_baseline()

        if not is_baseline(self.cleaned_data.get("subject_visit")):
            for reportable_field in ["reportable_as_ae", "patient_admitted"]:
                self.applicable_if(
                    YES, field="has_diagnoses", field_applicable=reportable_field
                )


class DiagnosesForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = DiagnosesFormValidator

    class Meta:
        model = Diagnoses
        fields = "__all__"
