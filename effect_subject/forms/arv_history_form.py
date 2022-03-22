from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator

from ..models import ArvHistory


class ArvHistoryFormValidator(FormValidator):
    pass


class ArvHistoryForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = ArvHistoryFormValidator

    class Meta:
        model = ArvHistory
        fields = "__all__"
