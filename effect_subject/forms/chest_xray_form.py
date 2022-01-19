from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator
from edc_glucose.form_validators import GlucoseFormValidatorMixin

from ..models import ChestXray


class ChestXrayFormValidator(GlucoseFormValidatorMixin, FormValidator):
    pass


class ChestXrayForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = ChestXrayFormValidator

    class Meta:
        model = ChestXray
        fields = "__all__"
