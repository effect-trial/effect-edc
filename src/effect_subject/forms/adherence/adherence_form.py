from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator

from ...models import Adherence


class AdherenceFormValidator(FormValidator):
    pass


class AdherenceForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = AdherenceFormValidator

    class Meta:
        model = Adherence
        fields = "__all__"
