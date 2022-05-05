from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from effect_form_validators.effect_subject import ArvTreatmentFormValidator

from ..models import ArvTreatment


class ArvTreatmentForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = ArvTreatmentFormValidator

    class Meta:
        model = ArvTreatment
        fields = "__all__"
