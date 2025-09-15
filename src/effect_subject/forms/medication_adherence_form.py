from django import forms
from edc_adherence.model_form_mixin import MedicationAdherenceFormMixin
from edc_crf.modelform_mixins import CrfModelFormMixin
from effect_form_validators.effect_subject import MedicationAdherenceFormValidator

from ..models import MedicationAdherence


class MedicationAdherenceForm(
    MedicationAdherenceFormMixin,
    CrfModelFormMixin,
    forms.ModelForm,
):
    form_validator_cls = MedicationAdherenceFormValidator

    class Meta:
        model = MedicationAdherence
        fields = "__all__"
