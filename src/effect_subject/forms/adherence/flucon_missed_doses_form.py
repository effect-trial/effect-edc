from django import forms
from edc_crf.modelform_mixins import InlineCrfModelFormMixin
from edc_form_validators import FormValidatorMixin
from effect_form_validators.effect_subject import FluconMissedDosesFormValidator

from ...models import FluconMissedDoses


class FluconMissedDosesForm(InlineCrfModelFormMixin, FormValidatorMixin, forms.ModelForm):
    form_validator_cls = FluconMissedDosesFormValidator

    class Meta:
        model = FluconMissedDoses
        fields = "__all__"
