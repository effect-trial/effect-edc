from django import forms
from edc_action_item.forms import ActionItemCrfFormMixin
from edc_crf.modelform_mixins import CrfModelFormMixin
from effect_form_validators.effect_subject import VitalSignsFormValidator

from ..models import VitalSigns


class VitalSignsForm(CrfModelFormMixin, ActionItemCrfFormMixin, forms.ModelForm):
    form_validator_cls = VitalSignsFormValidator

    class Meta(ActionItemCrfFormMixin.Meta):
        model = VitalSigns
        fields = "__all__"
