from django import forms
from edc_consent.form_validators import ConsentFormValidatorMixin
from edc_constants.constants import FEMALE, MALE, NO, OTHER, PENDING, POS, YES
from edc_form_validators import FormValidator


class SubjectScreeningFormValidator(ConsentFormValidatorMixin, FormValidator):
    def clean(self) -> None:
        self.get_consent_for_period_or_raise(self.cleaned_data.get("report_datetime"))
        self.validate_age()
        self.validate_cd4()
        self.validate_serum_crag()
        self.validate_lp_and_csf_crag()
        self.validate_cm_in_csf()
        self.validate_mg_ssx()
        self.validate_pregnancy()
        self.required_if(
            YES, field="unsuitable_for_study", field_required="reasons_unsuitable"
        )

    def validate_cd4(self) -> None:
        if self.cleaned_data.get("cd4_date") and self.cleaned_data.get("report_datetime"):
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
            ).days > 21:
                raise forms.ValidationError(
                    {
                        "cd4_date": (
                            "Invalid. Cannot be more than 21 days before the report date"
                        )
                    }
                )

    def validate_serum_crag(self) -> None:
        """Assert serum CrAg date is:
        - positive
        - not before CD4 date
        - within 21 days of CD4
        - within 14 days of report
        """
        if self.cleaned_data.get("serum_crag_value") != POS:
            raise forms.ValidationError(
                {
                    "serum_crag_value": (
                        "Invalid. Subject must have positive serum/plasma CrAg test result."
                    )
                }
            )

        if self.cleaned_data.get("serum_crag_date") and self.cleaned_data.get("cd4_date"):

            days = (
                self.cleaned_data.get("cd4_date") - self.cleaned_data.get("serum_crag_date")
            ).days

            if days > 0:
                raise forms.ValidationError(
                    {"serum_crag_date": "Invalid. Cannot be before CD4 date."}
                )
            if not 0 <= abs(days) <= 21:
                days = (
                    self.cleaned_data.get("serum_crag_date")
                    - self.cleaned_data.get("cd4_date")
                ).days
                raise forms.ValidationError(
                    {
                        "serum_crag_date": (
                            "Invalid. Must have been performed within 21 days "
                            f"of CD4. Got {days}."
                        )
                    }
                )
            if (
                self.cleaned_data.get("report_datetime").date()
                - self.cleaned_data.get("serum_crag_date")
            ).days > 14:
                raise forms.ValidationError(
                    {
                        "serum_crag_date": (
                            "Invalid. Cannot be more than 14 days before the report date"
                        )
                    }
                )

    def validate_lp_and_csf_crag(self) -> None:
        self.required_if(YES, field="lp_done", field_required="lp_date")

        if (
            self.cleaned_data.get("lp_date")
            and self.cleaned_data.get("serum_crag_date")
            and (self.cleaned_data.get("lp_date") < self.cleaned_data.get("serum_crag_date"))
        ):
            raise forms.ValidationError(
                {"lp_date": "Invalid. Cannot be before serum CrAg date"}
            )

        if (
            self.cleaned_data.get("lp_date")
            and self.cleaned_data.get("lp_date")
            > self.cleaned_data.get("report_datetime").date()
        ):
            raise forms.ValidationError({"lp_date": "Invalid. Cannot be after report date"})

        self.applicable_if(NO, field="lp_done", field_applicable="lp_declined")

        self.applicable_if(YES, field="lp_done", field_applicable="csf_crag_value")

    def validate_cm_in_csf(self) -> None:
        self.applicable_if(YES, field="lp_done", field_applicable="cm_in_csf")
        self.required_if(PENDING, field="cm_in_csf", field_required="cm_in_csf_date")
        self.applicable_if(YES, field="cm_in_csf", field_applicable="cm_in_csf_method")
        self.required_if(
            OTHER, field="cm_in_csf_method", field_required="cm_in_csf_method_other"
        )
        if (
            self.cleaned_data.get("cm_in_csf_date")
            and self.cleaned_data.get("lp_date")
            and (self.cleaned_data.get("lp_date") > self.cleaned_data.get("cm_in_csf_date"))
        ):
            raise forms.ValidationError(
                {"cm_in_csf_date": "Invalid. Cannot be before LP date"}
            )
        if (
            self.cleaned_data.get("cm_in_csf_date")
            and self.cleaned_data.get("report_datetime")
            and (
                self.cleaned_data.get("report_datetime").date()
                > self.cleaned_data.get("cm_in_csf_date")
            )
        ):
            raise forms.ValidationError(
                {"cm_in_csf_date": "Invalid. Cannot be before report date"}
            )

    def validate_pregnancy(self) -> None:
        if self.cleaned_data.get("gender") == MALE and self.cleaned_data.get("pregnant") in [
            YES,
            NO,
        ]:
            raise forms.ValidationError({"pregnant": "Invalid. Subject is male"})
        if self.cleaned_data.get("gender") == MALE and self.cleaned_data.get("preg_test_date"):
            raise forms.ValidationError({"preg_test_date": "Invalid. Subject is male"})
        self.applicable_if(FEMALE, field="gender", field_applicable="breast_feeding")

    def validate_age(self) -> None:
        if self.cleaned_data.get("age_in_years") and (
            self.cleaned_data.get("age_in_years") < 18
            or self.cleaned_data.get("age_in_years") > 120
        ):
            raise forms.ValidationError(
                {"age_in_years": "Invalid. Subject must be 18 years or older"}
            )

    def validate_mg_ssx(self) -> None:
        self.validate_other_specify(
            field="any_other_mg_ssx",
            other_specify_field="any_other_mg_ssx_other",
            other_stored_value=YES,
        )
