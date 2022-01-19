from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator
from edc_glucose.form_validators import GlucoseFormValidatorMixin

from ..models import MentalStatus


class MentalStatusFormValidator(GlucoseFormValidatorMixin, FormValidator):
    pass


class MentalStatusForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = MentalStatusFormValidator

    class Meta:
        model = MentalStatus
        fields = "__all__"
