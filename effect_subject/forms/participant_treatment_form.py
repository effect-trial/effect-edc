from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from effect_form_validators.effect_subject import ParticipantTreatmentFormValidator

from ..models import ParticipantTreatment


class ParticipantTreatmentForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = ParticipantTreatmentFormValidator

    class Meta:
        model = ParticipantTreatment
        fields = "__all__"
