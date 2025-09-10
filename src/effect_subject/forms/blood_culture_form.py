from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from effect_form_validators.effect_subject import BloodCultureFormValidator

from ..models import BloodCulture


class BloodCultureForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = BloodCultureFormValidator

    class Meta:
        model = BloodCulture
        fields = "__all__"
