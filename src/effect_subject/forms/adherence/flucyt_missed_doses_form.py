from django import forms
from edc_crf.modelform_mixins import InlineCrfModelFormMixin
from edc_form_validators import FormValidatorMixin
from effect_form_validators.effect_subject import FlucytMissedDosesFormValidator

from ...models import FlucytMissedDoses


class FlucytMissedDosesForm(InlineCrfModelFormMixin, FormValidatorMixin, forms.ModelForm):
    form_validator_cls = FlucytMissedDosesFormValidator

    class Meta:
        model = FlucytMissedDoses
        fields = "__all__"
