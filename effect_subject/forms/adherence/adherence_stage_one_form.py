from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator

from ...models import AdherenceStageOne


class AdherenceStageOneFormValidator(FormValidator):
    pass


class AdherenceStageOneForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = AdherenceStageOneFormValidator

    class Meta:
        model = AdherenceStageOne
        fields = "__all__"
