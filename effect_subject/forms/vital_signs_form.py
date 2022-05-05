from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_crf.modelform_mixins import CrfModelFormMixin
from effect_form_validators.effect_subject import VitalSignsFormValidator

from ..models import VitalSigns


class VitalSignsForm(CrfModelFormMixin, ActionItemFormMixin, forms.ModelForm):
    form_validator_cls = VitalSignsFormValidator

    class Meta:
        model = VitalSigns
        fields = "__all__"
