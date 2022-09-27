from django import forms
from edc_protocol_incident.forms import ProtocolDeviationViolationForm as Base

from ..models import ProtocolDeviationViolation


class ProtocolDeviationViolationForm(Base):
    class Meta:
        model = ProtocolDeviationViolation
        fields = "__all__"
        help_text = {"subject_identifier": "(read-only)", "action_identifier": "(read-only)"}
        widgets = {
            "subject_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
            "action_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
        }
