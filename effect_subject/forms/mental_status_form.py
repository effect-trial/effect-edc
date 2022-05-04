from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from effect_form_validators.effect_subject import MentalStatusFormValidator

from ..models import MentalStatus


class MentalStatusForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = MentalStatusFormValidator

    class Meta:
        model = MentalStatus
        fields = "__all__"
