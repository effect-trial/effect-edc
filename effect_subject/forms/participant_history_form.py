from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from effect_form_validators.effect_subject import ParticipantHistoryFormValidator

from ..models import ParticipantHistory


class ParticipantHistoryForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = ParticipantHistoryFormValidator

    class Meta:
        model = ParticipantHistory
        fields = "__all__"
