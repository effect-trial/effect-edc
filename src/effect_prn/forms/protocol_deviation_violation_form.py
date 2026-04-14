from django import forms
from edc_protocol_incident.form_validators import (
    ProtocolDeviationViolationFormValidator as BaseProtocolDeviationViolationFormValidator,
)
from edc_protocol_incident.forms import ProtocolDeviationViolationForm as Base

from ..constants import REMAIN_ON_STUDY_MODIFIED
from ..models import ProtocolDeviationViolation


class ProtocolDeviationViolationFormValidator(BaseProtocolDeviationViolationFormValidator):
    def validate_action(self):
        self.required_if(
            REMAIN_ON_STUDY_MODIFIED,
            field="action_required",
            field_required="action_required_followup",
        )


class ProtocolDeviationViolationForm(Base):
    form_validator_cls = ProtocolDeviationViolationFormValidator

    class Meta:
        model = ProtocolDeviationViolation
        fields = "__all__"
        help_text = {"subject_identifier": "(read-only)", "action_identifier": "(read-only)"}  # noqa: RUF012
        widgets = {  # noqa: RUF012
            "subject_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
            "action_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
        }
