from django import forms
from edc_adverse_event.modelform_mixins import DeathReportTmgModelFormMixin

from ..form_validators import DeathReportTmgFormValidator
from ..models import DeathReportTmg


class DeathReportTmgForm(DeathReportTmgModelFormMixin, forms.ModelForm):
    form_validator_cls = DeathReportTmgFormValidator

    class Meta(DeathReportTmgModelFormMixin.Meta):
        model = DeathReportTmg
        fields = "__all__"
