from django import forms
from edc_adverse_event.modelform_mixins import DeathReportModelFormMixin
from effect_form_validators.effect_ae import DeathReportFormValidator

from ..models import DeathReport


class DeathReportForm(DeathReportModelFormMixin, forms.ModelForm):
    form_validator_cls = DeathReportFormValidator

    class Meta(DeathReportModelFormMixin.Meta):
        model = DeathReport
        fields = "__all__"
