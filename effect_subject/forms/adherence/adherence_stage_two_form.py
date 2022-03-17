from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator

from ...models import AdherenceStageTwo


class AdherenceStageTwoFormValidator(FormValidator):
    pass


class AdherenceStageTwoForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = AdherenceStageTwoFormValidator

    class Meta:
        model = AdherenceStageTwo
        fields = "__all__"
