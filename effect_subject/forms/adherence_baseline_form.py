from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator

from ..models import AdherenceBaseline


class AdherenceBaselineFormValidator(FormValidator):
    pass


class AdherenceBaselineForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = AdherenceBaselineFormValidator

    class Meta:
        model = AdherenceBaseline
        fields = "__all__"
