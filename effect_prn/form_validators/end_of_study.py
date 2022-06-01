from edc_adverse_event.form_validator_mixins import (
    RequiresDeathReportFormValidatorMixin,
)
from edc_consent.constants import CONSENT_WITHDRAWAL
from edc_constants.constants import OTHER, YES
from edc_form_validators import FormValidator

from ..constants import CARE_TRANSFERRED_OUT, LATE_EXCLUSION_OTHER


class EndOfStudyFormValidator(
    RequiresDeathReportFormValidatorMixin,
    FormValidator,
):
    death_report_model = "effect_ae.deathreport"
    ltfu_model = None

    def clean(self):

        self.required_if(YES, field="cm_admitted", field_required="cm_admitted_cnt")

        self.required_if(
            OTHER, field="offschedule_reason", field_required="offschedule_reason_other"
        )

        self.required_if(
            CONSENT_WITHDRAWAL,
            field="offschedule_reason",
            field_required="withdrawal_consent_reasons",
        )

        self.required_if(
            LATE_EXCLUSION_OTHER,
            field="offschedule_reason",
            field_required="late_exclusion_other",
        )

        self.applicable_if(
            CARE_TRANSFERRED_OUT,
            field="offschedule_reason",
            field_applicable="transferred_consent",
        )
