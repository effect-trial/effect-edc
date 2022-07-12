from edc_adverse_event.form_validator_mixins import (
    RequiresDeathReportFormValidatorMixin,
)
from edc_consent.constants import CONSENT_WITHDRAWAL
from edc_constants.constants import DEAD, OTHER
from edc_form_validators import FormValidator
from edc_ltfu.constants import LOST_TO_FOLLOWUP
from edc_ltfu.modelform_mixins import RequiresLtfuFormValidatorMixin


class EndOfStudyFormValidator(
    RequiresDeathReportFormValidatorMixin,
    RequiresLtfuFormValidatorMixin,
    FormValidator,
):
    death_report_model = "effect_ae.deathreport"
    offschedule_reason_field = "offschedule_reason"
    ltfu_model = "effect_prn.losstofollowup"
    ltfu_date_field = "ltfu_date"

    def clean(self):

        self.validate_death_report_if_deceased()
        self.validate_ltfu()

        self.validate_other_specify(
            field="offschedule_reason",
            other_specify_field="other_offschedule_reason",
            other_stored_value=OTHER,
        )

        self.required_if(DEAD, field="offschedule_reason", field_required="death_date")

        self.required_if(
            LOST_TO_FOLLOWUP,
            field="offschedule_reason",
            field_required="ltfu_date",
        )

        self.required_if(
            CONSENT_WITHDRAWAL,
            field="offschedule_reason",
            field_required="consent_withdrawal_reason",
        )

        self.required_if(
            "included_in_error",
            field="offschedule_reason",
            field_required="included_in_error",
        )

        self.required_if(
            "included_in_error",
            field="offschedule_reason",
            field_required="included_in_error_date",
        )
