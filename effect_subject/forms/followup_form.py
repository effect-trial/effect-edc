from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_constants.constants import DEAD, HOSPITAL_NOTES, NOT_APPLICABLE, OTHER
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator

from ..choices import ASSESSMENT_INFO_SOURCES, ASSESSMENT_TYPES, INFO_SOURCE
from ..constants import (
    COLLATERAL_HISTORY,
    IN_PERSON,
    NEXT_OF_KIN,
    OUTPATIENT_CARDS,
    PATIENT,
    TELEPHONE,
)
from ..models import Followup


def get_choice_display_text(choices: tuple[tuple[str, str]], key: str) -> str:
    """Returns display text given a choices tuple and lookup key."""
    return dict(choices).get(key)


class FollowupFormValidator(FormValidator):
    def clean(self):
        self.validate_other_specify(field="assessment_type")

        self.applicable_if(
            TELEPHONE, field="assessment_type", field_applicable="info_source"
        )
        self.validate_other_specify(field="info_source")

        self.validate_against_subject_visit_info_source()

        self.validate_survival_status()

        self.not_applicable_if(
            DEAD,
            field="survival_status",
            field_applicable="adherence_counselling",
            not_applicable_msg=(
                "Invalid: Expected 'Not applicable' if survival status is 'Deceased'"
            ),
        )

    @staticmethod
    def sv_info_source_reconciles_with_fu(
        sv_info_source: str,
        fu_assessment_type: str,
        fu_info_source: str,
    ) -> bool:
        """Returns True, if Subject Visit 'info_source' answer reconciles with
        Follow-up 'assessment_type' and 'info_source' answers.
        """
        return (
            sv_info_source == PATIENT
            and any(
                (
                    fu_assessment_type == IN_PERSON
                    and fu_info_source == NOT_APPLICABLE,
                    fu_assessment_type == TELEPHONE and fu_info_source == PATIENT,
                )
            )
            or sv_info_source == COLLATERAL_HISTORY
            and any(
                (
                    fu_assessment_type == TELEPHONE and fu_info_source == NEXT_OF_KIN,
                    fu_assessment_type == TELEPHONE and fu_info_source == OTHER,
                    # TODO: Is assessment_type OTHER ok with COLLATERAL_HISTORY?
                    #  (it is currently)
                    fu_assessment_type == OTHER and fu_info_source == NOT_APPLICABLE,
                )
            )
            or (
                # TODO: Can any of the following be with assessment_type TELEPHONE?
                #  (none are currently)
                sv_info_source == HOSPITAL_NOTES
                or sv_info_source == OUTPATIENT_CARDS
                or sv_info_source == OTHER
            )
            and any((fu_assessment_type == OTHER and fu_info_source == NOT_APPLICABLE,))
        )

    @staticmethod
    def get_sv_info_source_mismatch_error_msg(
        sv_info_source: str,
        fu_assessment_type: str,
        fu_info_source: str,
    ) -> str:
        return (
            "Invalid. Did not expect "
            f"'{get_choice_display_text(ASSESSMENT_TYPES, fu_assessment_type)}' "
            "assessment with "
            f"'{get_choice_display_text(ASSESSMENT_INFO_SOURCES, fu_info_source)}'"
            f", since the main source of information provided in the Subject Visit was "
            f"'{get_choice_display_text(INFO_SOURCE, sv_info_source)}'."
        )

    def validate_against_subject_visit_info_source(self):
        sv_info_source = self.cleaned_data.get("subject_visit").info_source
        fu_assessment_type = self.cleaned_data.get("assessment_type")
        fu_info_source = self.cleaned_data.get("info_source")

        if not self.sv_info_source_reconciles_with_fu(
            sv_info_source=sv_info_source,
            fu_assessment_type=fu_assessment_type,
            fu_info_source=fu_info_source,
        ):
            error_msg = self.get_sv_info_source_mismatch_error_msg(
                sv_info_source=sv_info_source,
                fu_assessment_type=fu_assessment_type,
                fu_info_source=fu_info_source,
            )
            raise forms.ValidationError(
                {
                    "assessment_type": error_msg,
                    "info_source": error_msg,
                }
            )

    def validate_survival_status(self):
        if (
            self.cleaned_data.get("survival_status") == DEAD
            and self.cleaned_data.get("assessment_type") == IN_PERSON
        ):
            raise forms.ValidationError(
                {
                    "survival_status": (
                        "Invalid: Unexpected survival status 'Deceased' if "
                        "'In person' visit"
                    )
                }
            )
        elif (
            self.cleaned_data.get("survival_status") == DEAD
            and self.cleaned_data.get("assessment_type") == TELEPHONE
            and self.cleaned_data.get("info_source") == PATIENT
        ):
            raise forms.ValidationError(
                {
                    "survival_status": (
                        "Invalid: Unexpected survival status 'Deceased' if "
                        "'Telephone' visit with 'Patient'"
                    )
                }
            )


class FollowupForm(CrfModelFormMixin, ActionItemFormMixin, forms.ModelForm):
    form_validator_cls = FollowupFormValidator

    class Meta:
        model = Followup
        fields = "__all__"
