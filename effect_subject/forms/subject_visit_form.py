from django import forms
from django.utils.translation import gettext_lazy as _
from edc_constants.choices import ALIVE_DEAD_UNKNOWN
from edc_constants.constants import ALIVE, HOSPITAL_NOTES, OTHER, UNKNOWN, YES
from edc_constants.utils import get_display
from edc_form_validators import FormValidatorMixin
from edc_sites.forms import SiteModelFormMixin
from edc_visit_schedule.constants import DAY1
from edc_visit_tracking.form_validators import VisitFormValidator

from ..choices import ASSESSMENT_TYPES, ASSESSMENT_WHO_CHOICES, INFO_SOURCE
from ..constants import (
    IN_PERSON,
    NEXT_OF_KIN,
    OUTPATIENT_CARDS,
    PATIENT,
    PATIENT_REPRESENTATIVE,
    TELEPHONE,
)
from ..models import SubjectVisit


class SubjectVisitFormValidator(VisitFormValidator):
    validate_missed_visit_reason = False

    @staticmethod
    def is_baseline_appointment(appointment) -> bool:
        return appointment.visit_code == DAY1 and appointment.visit_code_sequence == 0

    def clean(self):
        super().clean()
        self.validate_assessment_type()

        self.validate_assessment_who()

        self.validate_info_source_against_assessment_type_who()

        self.validate_survival_status()

        self.validate_hospitalized()

    def validate_assessment_type(self):
        if (
            self.is_baseline_appointment(self.cleaned_data.get("appointment"))
            and self.cleaned_data.get("assessment_type") != IN_PERSON
        ):
            raise forms.ValidationError(
                {"assessment_type": "Invalid. Expected 'In person' at baseline"}
            )

        self.validate_other_specify(field="assessment_type")

    def validate_assessment_who(self):
        if (
            self.cleaned_data.get("assessment_type") == IN_PERSON
            and self.cleaned_data.get("assessment_who") != PATIENT
        ):
            raise forms.ValidationError(
                {"assessment_who": "Invalid. Expected 'Patient' if 'In person' visit"}
            )

        self.validate_other_specify(field="assessment_who")

    @staticmethod
    def info_source_reconciles_with_assessment_type_who(
        info_source: str,
        assessment_type: str,
        assessment_who: str,
    ) -> bool:
        """Returns True, if 'info_source' answer reconciles with
        'assessment_type' and 'assessment_who' answers.
        """
        return (
            info_source == PATIENT
            and any(
                (
                    assessment_type == IN_PERSON and assessment_who == PATIENT,
                    assessment_type == TELEPHONE and assessment_who == PATIENT,
                )
            )
            or info_source == PATIENT_REPRESENTATIVE
            and any(
                (
                    assessment_type == TELEPHONE and assessment_who == NEXT_OF_KIN,
                    assessment_type == TELEPHONE and assessment_who == OTHER,
                    assessment_type == OTHER,
                )
            )
            or info_source in [HOSPITAL_NOTES, OUTPATIENT_CARDS, OTHER]
        )

    @staticmethod
    def get_info_source_mismatch_error_msg(
        info_source: str,
        assessment_type: str,
        assessment_who: str,
    ) -> str:
        return (
            "Invalid. Did not expect information source: "
            f"'{get_display(INFO_SOURCE, info_source)}' for "
            f"'{get_display(ASSESSMENT_TYPES, assessment_type)}' "
            "assessment with "
            f"'{get_display(ASSESSMENT_WHO_CHOICES, assessment_who)}.'"
        )

    def validate_info_source_against_assessment_type_who(self):
        if not self.info_source_reconciles_with_assessment_type_who(
            info_source=self.cleaned_data.get("info_source"),
            assessment_type=self.cleaned_data.get("assessment_type"),
            assessment_who=self.cleaned_data.get("assessment_who"),
        ):
            error_msg = self.get_info_source_mismatch_error_msg(
                info_source=self.cleaned_data.get("info_source"),
                assessment_type=self.cleaned_data.get("assessment_type"),
                assessment_who=self.cleaned_data.get("assessment_who"),
            )
            raise forms.ValidationError({"info_source": error_msg})

    def validate_survival_status(self):
        if self.cleaned_data.get("survival_status") != ALIVE:
            error_msg = None

            if self.is_baseline_appointment(self.cleaned_data.get("appointment")):
                survival_status = get_display(
                    ALIVE_DEAD_UNKNOWN, self.cleaned_data.get("survival_status")
                )
                error_msg = f"Invalid: Cannot be '{survival_status}' at baseline"

            elif self.cleaned_data.get("assessment_type") == IN_PERSON:
                error_msg = "Invalid: Expected 'Alive' if this is an 'In person' visit"

            elif self.cleaned_data.get("assessment_who") == PATIENT:
                error_msg = "Invalid: Expected 'Alive' if spoke to 'Patient'"

            if error_msg:
                raise forms.ValidationError({"survival_status": error_msg})

    def validate_hospitalized(self):
        if (
            self.is_baseline_appointment(self.cleaned_data.get("appointment"))
            and self.cleaned_data.get("hospitalized") == YES
        ):
            raise forms.ValidationError(
                {"hospitalized": "Invalid. Expected NO at baseline"}
            )

        if self.cleaned_data.get("hospitalized") == UNKNOWN and (
            self.cleaned_data.get("assessment_who") == PATIENT
            or self.cleaned_data.get("info_source") == PATIENT
        ):
            raise forms.ValidationError(
                {
                    "hospitalized": (
                        "Invalid. Cannot be 'Unknown' if spoke to 'Patient' "
                        "or 'Patient' was MAIN source of information"
                    )
                }
            )


class SubjectVisitForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = SubjectVisitFormValidator

    class Meta:
        model = SubjectVisit
        fields = "__all__"
        help_texts = {
            "survival_status": _("If subject deceased, complete Death report"),
        }
