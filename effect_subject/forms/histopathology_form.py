from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from effect_form_validators.effect_subject import HistopathologyFormValidator

from ..models import Histopathology


class HistopathologyForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = HistopathologyFormValidator

    class Meta:
        model = Histopathology
        fields = "__all__"
