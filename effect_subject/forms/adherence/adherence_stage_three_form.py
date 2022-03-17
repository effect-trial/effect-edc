from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator

from ...models import AdherenceStageThree


class AdherenceStageThreeFormValidator(FormValidator):
    pass


class AdherenceStageThreeForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = AdherenceStageThreeFormValidator

    class Meta:
        model = AdherenceStageThree
        fields = "__all__"
