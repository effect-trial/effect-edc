from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator
from edc_glucose.form_validators import GlucoseFormValidatorMixin

from ..models import ArvTreatment


class ArvTreatmentFormValidator(GlucoseFormValidatorMixin, FormValidator):
    pass


class ArvTreatmentForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = ArvTreatmentFormValidator

    class Meta:
        model = ArvTreatment
        fields = "__all__"
