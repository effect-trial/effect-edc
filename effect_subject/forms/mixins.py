from django import forms
from edc_constants.constants import NO, NOT_APPLICABLE, OTHER, YES
from edc_visit_schedule.utils import is_baseline


class ArvHistoryFormValidatorMixin:
    def validate_arv_history_fields(self):
        self.date_not_before(
            "arv_initiation_date",
            "viral_load_date",
            "Invalid. Cannot be before ARV initiation date.",
        )

        self.date_not_before(
            "arv_initiation_date",
            "current_arv_regimen_date",
            "Invalid. Cannot be before ARV initiation date.",
        )

        self.required_if_not_none(
            "viral_load", "viral_load_date", field_required_evaluate_as_int=True
        )

        self.date_not_before(
            "hiv_diagnosis_date",
            "viral_load_date",
            "Invalid. Cannot be before HIV diagnosis date.",
        )

        self.required_if_not_none(
            "cd4", "cd4_date", field_required_evaluate_as_int=True
        )

        self.date_not_before(
            "hiv_diagnosis_date",
            "cd4_date",
            "Invalid. Cannot be before HIV diagnosis date.",
        )

        self.required_if(
            OTHER,
            field="current_arv_regimen",
            field_required="other_current_arv_regimen",
        )

        self.required_if(
            YES, field="has_previous_arv_regimen", field_required="previous_arv_regimen"
        )

        if self.cleaned_data.get("has_previous_arv_regimen") == NO:
            self.date_equal(
                "arv_initiation_date",
                "current_arv_regimen_start_date",
                "Invalid. Expected current regimen date to equal initiation date.",
            )

        self.required_if(
            YES, field="has_previous_arv_regimen", field_required="previous_arv_regimen"
        )

        self.required_if(
            OTHER,
            field="previous_arv_regimen",
            field_required="other_previous_arv_regimen",
        )

        self.required_if(
            YES, field="on_oi_prophylaxis", field_required="oi_prophylaxis"
        )

        self.m2m_other_specify(
            OTHER, m2m_field="oi_prophylaxis", field_other="other_oi_prophylaxis"
        )


class ReportingFieldsetFormValidatorMixin:
    reportable_fields = ["reportable_as_ae", "patient_admitted"]

    def validate_reporting_fieldset(self):
        self.validate_reporting_fieldset_na_baseline()
        self.validate_reporting_fieldset_applicable_if_not_baseline()

    def validate_field_na_baseline(self, field_applicable: str):
        if (
            is_baseline(self.cleaned_data.get("subject_visit"))
            and self.cleaned_data.get(field_applicable) != NOT_APPLICABLE
        ):
            raise forms.ValidationError(
                {field_applicable: "This field is not applicable at baseline."}
            )

    def validate_reporting_fieldset_na_baseline(self):
        for reportable_field in self.reportable_fields:
            self.validate_field_na_baseline(field_applicable=reportable_field)

    def validate_reporting_fieldset_applicable_if_not_baseline(self):
        for reportable_field in self.reportable_fields:
            self.applicable_if_true(
                condition=not is_baseline(self.cleaned_data.get("subject_visit")),
                field_applicable=reportable_field,
            )
