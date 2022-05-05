from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_crf.modelform_mixins import CrfModelFormMixin
from effect_form_validators.effect_subject import FollowupFormValidator

from ..models import Followup


class FollowupForm(CrfModelFormMixin, ActionItemFormMixin, forms.ModelForm):
    form_validator_cls = FollowupFormValidator

    class Meta:
        model = Followup
        fields = "__all__"
