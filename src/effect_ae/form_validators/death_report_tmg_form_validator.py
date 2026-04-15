from clinicedc_constants import CLOSED, NOT_EVALUATED
from edc_adverse_event.form_validators import (
    DeathReportTmgFormValidator as BaseDeathReportTmgFormValidator,
)


class DeathReportTmgFormValidator(BaseDeathReportTmgFormValidator):
    def validate_before_report_status(self):
        self.required_if(
            CLOSED,
            field="report_status",
            field_required="cryptococcal_relatedness",
            inverse=False,
        )
        self.required_if_true(
            self.cleaned_data.get("cryptococcal_relatedness") != NOT_EVALUATED,
            field_required="cryptococcal_relatedness_comment",
        )
