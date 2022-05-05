from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from effect_form_validators.effect_subject import ArvHistoryFormValidator

from ..models import ArvHistory


class ArvHistoryForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = ArvHistoryFormValidator

    class Meta:
        model = ArvHistory
        fields = "__all__"
