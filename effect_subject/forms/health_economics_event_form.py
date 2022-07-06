from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator

from ..models import HealthEconomicsEvent


class HealthEconomicsEventFormValidator(FormValidator):
    pass


class HealthEconomicsEventForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = HealthEconomicsEventFormValidator

    class Meta:
        model = HealthEconomicsEvent
        fields = "__all__"
