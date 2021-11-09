from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator
from edc_glucose.form_validators import GlucoseFormValidatorMixin

from ..models import StudyTreatmentDay14


class StudyTreatmentDay14FormValidator(GlucoseFormValidatorMixin, FormValidator):
    pass


class StudyTreatmentDay14Form(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = StudyTreatmentDay14FormValidator

    class Meta:
        model = StudyTreatmentDay14
        fields = "__all__"
