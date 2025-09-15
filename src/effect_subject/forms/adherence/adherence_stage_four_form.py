from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator

from ...models import AdherenceStageFour


class AdherenceStageFourFormValidator(FormValidator):
    pass


class AdherenceStageFourForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = AdherenceStageFourFormValidator

    class Meta:
        model = AdherenceStageFour
        fields = "__all__"
