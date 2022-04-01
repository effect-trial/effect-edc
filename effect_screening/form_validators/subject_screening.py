from django import forms
from edc_consent.form_validators import ConsentFormValidatorMixin
from edc_constants.constants import FEMALE, IND, MALE, NEG, NO, OTHER, PENDING, POS, YES
from edc_form_validators import FormValidator


class SubjectScreeningFormValidator(ConsentFormValidatorMixin, FormValidator):
    def clean(self):
        self.get_consent_for_period_or_raise(self.cleaned_data.get("report_datetime"))
        self.validate_age()
        self.validate_cd4()
        self.validate_serum_crag()
        self.validate_lp_and_csf_crag()
        self.validate_cm_in_csf()
        self.validate_ssx()
        self.validate_pregnancy()
        self.required_if(
            YES, field="unsuitable_for_study", field_required="reasons_unsuitable"
        )

    def validate_cd4(self):
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
            ).days > 21:
                raise forms.ValidationError(
                    {
                        "cd4_date": (
                            "Invalid. Cannot be more than 21 days before the report date"
                        )
                    }
                )

    def validate_serum_crag(self):
        """Assert serum CrAg date is:
        - not before CD4 date
        - within 21 days of CD4
        - within 14 days of report
        """
        self.required_if(
            POS, NEG, IND, field="serum_crag_value", field_required="serum_crag_date"
        )

        if self.cleaned_data.get("serum_crag_date") and self.cleaned_data.get(
            "cd4_date"
        ):

            days = (
                self.cleaned_data.get("cd4_date")
                - self.cleaned_data.get("serum_crag_date")
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

    def validate_lp_and_csf_crag(self):
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

    def validate_cm_in_csf(self):
        self.applicable_if(YES, field="lp_done", field_applicable="cm_in_csf")
        self.required_if(PENDING, field="cm_in_csf", field_required="cm_in_csf_date")
        self.applicable_if(YES, field="cm_in_csf", field_applicable="cm_in_csf_method")
        self.required_if(
            OTHER, field="cm_in_csf_method", field_required="cm_in_csf_method_other"
        )
        if (
            self.cleaned_data.get("cm_in_csf_date")
            and self.cleaned_data.get("lp_date")
            and (
                self.cleaned_data.get("lp_date")
                > self.cleaned_data.get("cm_in_csf_date")
            )
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

    def validate_pregnancy(self):
        if self.cleaned_data.get("gender") == MALE and self.cleaned_data.get(
            "pregnant"
        ) in [YES, NO]:
            raise forms.ValidationError({"pregnant": "Invalid. Subject is male"})
        if self.cleaned_data.get("gender") == MALE and self.cleaned_data.get(
            "preg_test_date"
        ):
            raise forms.ValidationError({"preg_test_date": "Invalid. Subject is male"})
        self.applicable_if(FEMALE, field="gender", field_applicable="breast_feeding")

    def validate_age(self):
        if self.cleaned_data.get("age_in_years") and (
            self.cleaned_data.get("age_in_years") < 18
            or self.cleaned_data.get("age_in_years") > 120
        ):
            raise forms.ValidationError(
                {"age_in_years": "Invalid. Subject must be 18 years or older"}
            )

    def validate_ssx(self):
        self.m2m_required_if(YES, field="mg_ssx_since_crag", m2m_field="mg_ssx")
        self.m2m_other_specify(m2m_field="mg_ssx", field_other="mg_ssx_other")
