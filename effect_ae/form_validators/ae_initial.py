from django import forms
from edc_adverse_event.choices import AE_GRADE, STUDY_DRUG_RELATIONSHIP
from edc_adverse_event.form_validators import AeInitialFormValidator as FormValidator
from edc_constants.choices import YES_NO_UNKNOWN
from edc_constants.constants import DECEASED, NO, UNKNOWN, YES
from edc_reportable import GRADE5

from effect_ae.choices import INPATIENT_STATUSES
from effect_ae.constants import (
    DEFINITELY_RELATED,
    DISCHARGED,
    INPATIENT,
    POSSIBLY_RELATED,
    PROBABLY_RELATED,
    UNLIKELY_RELATED,
)
from effect_subject.forms.followup_form import get_choice_display_text


class AeInitialFormValidator(FormValidator):
    def clean(self):
        super().clean()
        self.validate_hospitalization()
        self.validate_study_relation_possibility()

    def validate_hospitalization(self):
        self.required_if(YES, field="patient_admitted", field_required="date_admitted")
        self.applicable_if(
            YES, field="patient_admitted", field_applicable="inpatient_status"
        )
        self.required_if(
            DISCHARGED, field="inpatient_status", field_required="date_discharged"
        )

        g5_display_text = get_choice_display_text(
            choices=AE_GRADE,
            key=GRADE5,
        )
        inpatient_status_display_text = get_choice_display_text(
            choices=INPATIENT_STATUSES,
            key=self.cleaned_data.get("inpatient_status"),
        )
        if (
            self.cleaned_data.get("inpatient_status") == INPATIENT
            and self.cleaned_data.get("ae_grade") == GRADE5
        ):
            raise forms.ValidationError(
                {
                    "inpatient_status": (
                        f"Invalid. Status cannot be '{inpatient_status_display_text}' "
                        f"if severity of AE is '{g5_display_text}'"
                    )
                }
            )
        if (
            self.cleaned_data.get("inpatient_status") == DECEASED
            and not self.cleaned_data.get("ae_grade") == GRADE5
        ):
            raise forms.ValidationError(
                {
                    "inpatient_status": (
                        f"Invalid. Status cannot be '{inpatient_status_display_text}' "
                        f"if severity of AE is not '{g5_display_text}'"
                    )
                }
            )

        if (
            self.cleaned_data.get("date_discharged")
            and self.cleaned_data.get("date_admitted")
            and self.cleaned_data.get("date_discharged")
            < self.cleaned_data.get("date_admitted")
        ):
            raise forms.ValidationError(
                {
                    "date_discharged": (
                        "Invalid. Date discharged cannot be before date admitted"
                    )
                }
            )

    def validate_study_relation_possibility(self):
        for study_drug in ["fluconazole", "flucytosine"]:
            if (
                self.cleaned_data.get("ae_study_relation_possibility") == NO
                and self.cleaned_data.get(f"{study_drug}_relation")
                in [
                    UNLIKELY_RELATED,
                    POSSIBLY_RELATED,
                    PROBABLY_RELATED,
                    DEFINITELY_RELATED,
                ]
            ) or (
                self.cleaned_data.get("ae_study_relation_possibility") == UNKNOWN
                and (
                    self.cleaned_data.get(f"{study_drug}_relation")
                    == DEFINITELY_RELATED
                )
            ):
                study_relation = get_choice_display_text(
                    choices=YES_NO_UNKNOWN,
                    key=self.cleaned_data.get("ae_study_relation_possibility"),
                )
                drug_relation_choice = get_choice_display_text(
                    choices=STUDY_DRUG_RELATIONSHIP,
                    key=self.cleaned_data.get(f"{study_drug}_relation"),
                )
                raise forms.ValidationError(
                    {
                        "ae_study_relation_possibility": (
                            f"Invalid. "
                            f"Cannot be '{study_relation}' if '{drug_relation_choice}' "
                            f"to study drug: {study_drug.title()}"
                        )
                    }
                )

    def validate_relationship_to_study_drug(self):
        # TODO: Flucytosine only applicable if a study drug (i.e. on that arm of trial)
        pass
