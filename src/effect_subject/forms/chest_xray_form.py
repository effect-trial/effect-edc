from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from effect_form_validators.effect_subject import ChestXrayFormValidator

from ..models import ChestXray


class ChestXrayForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = ChestXrayFormValidator

    class Meta:
        model = ChestXray
        fields = "__all__"
