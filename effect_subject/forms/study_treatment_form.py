from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator
from edc_glucose.form_validators import GlucoseFormValidatorMixin

from ..models import StudyTreatment


class StudyTreatmentFormValidator(GlucoseFormValidatorMixin, FormValidator):
    pass


class StudyTreatmentForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = StudyTreatmentFormValidator

    class Meta:
        model = StudyTreatment
        fields = "__all__"
