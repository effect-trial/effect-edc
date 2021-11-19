import pdb

from django import forms
from edc_consent.form_validators import ConsentFormValidatorMixin
from edc_constants.constants import IND, MALE, NEG, NO, PENDING, POS, YES
from edc_form_validators import FormValidator


class SubjectScreeningFormValidator(ConsentFormValidatorMixin, FormValidator):
    def clean(self):

        self.get_consent_for_period_or_raise(self.cleaned_data.get("report_datetime"))

        # cd4
        # TODO: date of crag cannot precede cd4 date
        if self.cleaned_data.get("cd4_date") and self.cleaned_data.get(
            "report_datetime"
        ):
            if (
                self.cleaned_data.get("cd4_date")
                > self.cleaned_data.get("report_datetime").date()
            ):
                raise forms.ValidationError(
                    {"cd4_date": "Invalid. Cannot be after report date"}
                )
            if (
                self.cleaned_data.get("report_datetime").date()
                - self.cleaned_data.get("cd4_date")
            ).days > 14:
                raise forms.ValidationError(
                    {
                        "cd4_date": "Invalid. Cannot be more than 14 days before the report date"
                    }
                )

        # serum_crag
        self.required_if(
            POS, NEG, IND, field="serum_crag_value", field_required="serum_crag_date"
        )

        if self.cleaned_data.get("serum_crag_date") and self.cleaned_data.get(
            "cd4_date"
        ):

            days = (
                self.cleaned_data.get("serum_crag_date")
                - self.cleaned_data.get("cd4_date")
            ).days

            if days > 0:
                raise forms.ValidationError(
                    {"serum_crag_date": "Invalid. Cannot be after serum CrAg date."}
                )
            if not 0 <= abs(days) <= 14:
                days = (
                    self.cleaned_data.get("serum_crag_date")
                    - self.cleaned_data.get("cd4_date")
                ).days
                raise forms.ValidationError(
                    {
                        "serum_crag_date": f"Invalid. Must have been performed within 14 days or CD4. Got {days}."
                    }
                )

        # lp / CSF CrAg
        self.required_if(YES, field="lp_done", field_required="lp_date")

        if self.cleaned_data.get("lp_date") and self.cleaned_data.get(
            "lp_date"
        ) < self.cleaned_data.get("serum_crag_date"):
            raise forms.ValidationError(
                {"lp_date": "Invalid. Cannot be before serum CrAg date"}
            )

        if (
            self.cleaned_data.get("lp_date")
            and self.cleaned_data.get("lp_date")
            > self.cleaned_data.get("report_datetime").date()
        ):
            raise forms.ValidationError(
                {"lp_date": "Invalid. Cannot be after report date"}
            )

        self.applicable_if(NO, field="lp_done", field_applicable="lp_declined")

        self.applicable_if(YES, field="lp_done", field_applicable="csf_crag_value")

        # CM testing
        self.applicable_if(
            YES, PENDING, field="lp_done", field_applicable="csf_cm_evidence"
        )
        self.required_if(
            PENDING, field="csf_cm_evidence", field_required="csf_results_date"
        )
        if self.cleaned_data.get("csf_results_date") and (
            self.cleaned_data.get("csf_results_date")
            < self.cleaned_data.get("report_datetime").date()
        ):
            raise forms.ValidationError(
                {"csf_results_date": "Invalid. Cannot be before report date"}
            )

        # pregnancy
        if self.cleaned_data.get("gender") == MALE and self.cleaned_data.get(
            "pregnant_or_bf"
        ) in [YES, NO]:
            raise forms.ValidationError({"pregnant_or_bf": "Invalid. Subject is male"})

        self.not_applicable_if(
            MALE, field="gender", field_applicable="pregnant", inverse=False
        )

        self.required_if(
            YES, field="unsuitable_for_study", field_required="reasons_unsuitable"
        )
