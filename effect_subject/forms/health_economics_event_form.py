from django import forms
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import CrfModelFormMixin

from ..models import HealthEconomicsEvent


class HealthEconomicsEventFormValidator(CrfFormValidator):
    pass


class HealthEconomicsEventForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = HealthEconomicsEventFormValidator

    class Meta:
        model = HealthEconomicsEvent
        fields = "__all__"
