from django import forms
from edc_crf.crf_form_validator import CrfFormValidator
from edc_crf.modelform_mixins import CrfModelFormMixin

from ..models import HealthEconomics


class HealthEconomicsFormValidator(CrfFormValidator):
    pass


class HealthEconomicsForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = HealthEconomicsFormValidator

    class Meta:
        model = HealthEconomics
        fields = "__all__"
