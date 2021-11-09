from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator
from edc_glucose.form_validators import GlucoseFormValidatorMixin

from ..models import Followup


class FollowupFormValidator(GlucoseFormValidatorMixin, FormValidator):
    pass


class FollowupForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = FollowupFormValidator

    class Meta:
        model = Followup
        fields = "__all__"
