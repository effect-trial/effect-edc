from django import forms
from edc_adverse_event.choices import AE_GRADE, STUDY_DRUG_RELATIONSHIP
from edc_adverse_event.constants import (
    DEFINITELY_RELATED,
    DISCHARGED,
    INPATIENT,
    POSSIBLY_RELATED,
    PROBABLY_RELATED,
)
from edc_adverse_event.form_validators import AeInitialFormValidator as FormValidator
from edc_constants.choices import YES_NO_UNKNOWN
from edc_constants.constants import CONTROL, DECEASED, GRADE5, YES
from edc_constants.utils import get_display
from edc_randomization.utils import (
    get_assignment_description_for_subject,
    get_assignment_for_subject,
)

from ..choices import INPATIENT_STATUSES


class AeInitialFormValidator(FormValidator):
    def clean(self):
        self.validate_other_specify(field="ae_classification")

        self.required_if(YES, field="patient_admitted", field_required="date_admitted")
        self.validate_inpatient_status()
        self.validate_date_discharged()

        self.validate_study_relation_possibility()
        self.validate_flucyt_against_study_arm()

        self.required_if(YES, field="ae_cause", field_required="ae_cause_other")

        super().clean()

    def validate_inpatient_status(self):
        self.applicable_if(YES, field="patient_admitted", field_applicable="inpatient_status")
        self.required_if(
            DISCHARGED, field="inpatient_status", field_required="date_discharged"
        )

        g5_display = get_display(choices=AE_GRADE, label=GRADE5)
        inpatient_status_display = get_display(
            choices=INPATIENT_STATUSES,
            label=self.cleaned_data.get("inpatient_status"),
        )
        if (
            self.cleaned_data.get("inpatient_status") == INPATIENT
            and self.cleaned_data.get("ae_grade") == GRADE5
        ):
            raise forms.ValidationError(
                {
                    "inpatient_status": (
                        f"Invalid. Status cannot be '{inpatient_status_display}' "
                        f"if severity of AE is '{g5_display}'"
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
                        f"Invalid. Status cannot be '{inpatient_status_display}' "
                        f"if severity of AE is not '{g5_display}'"
                    )
                }
            )

    def validate_date_discharged(self):
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
        for study_drug in ["flucon", "flucyt"]:
            if (
                self.cleaned_data.get(f"{study_drug}_relation")
                in [
                    POSSIBLY_RELATED,
                    PROBABLY_RELATED,
                    DEFINITELY_RELATED,
                ]
                and self.cleaned_data.get("ae_study_relation_possibility") != YES
                # ) or (
                #     self.cleaned_data.get(f"{study_drug}_relation")
                #     in [
                #         NOT_RELATED,
                #         UNLIKELY_RELATED,
                #     ]
                #     and self.cleaned_data.get("ae_study_relation_possibility") == YES
            ):
                study_relation_display = get_display(
                    choices=YES_NO_UNKNOWN,
                    label=self.cleaned_data.get("ae_study_relation_possibility"),
                )
                drug_relation_display = get_display(
                    choices=STUDY_DRUG_RELATIONSHIP,
                    label=self.cleaned_data.get(f"{study_drug}_relation"),
                )
                raise forms.ValidationError(
                    {
                        "ae_study_relation_possibility": (
                            f"Invalid. Cannot be '{study_relation_display}' "
                            f"if '{drug_relation_display}' "
                            f"to study drug: {study_drug.title()}"
                        )
                    }
                )

    def validate_flucyt_against_study_arm(self):
        assignment = get_assignment_for_subject(
            subject_identifier=self.cleaned_data.get("subject_identifier"),
            randomizer_name="default",
        )
        assignment_description = get_assignment_description_for_subject(
            subject_identifier=self.cleaned_data.get("subject_identifier"),
            randomizer_name="default",
        )

        self.not_applicable_if_true(
            assignment == CONTROL,
            field_applicable="flucyt_relation",
            not_applicable_msg=f"Participant is on {CONTROL} arm ({assignment_description}).",
        )
