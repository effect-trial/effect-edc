from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator
from edc_glucose.form_validators import GlucoseFormValidatorMixin

from ..models import Neurological


class NeurologicalFormValidator(GlucoseFormValidatorMixin, FormValidator):
    pass


class NeurologicalForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = NeurologicalFormValidator

    class Meta:
        model = Neurological
        fields = "__all__"
