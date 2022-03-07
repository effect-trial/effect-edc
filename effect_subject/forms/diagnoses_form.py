from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator

from ..models import Diagnoses
from .mixins import ReportingFieldsetFormValidatorMixin


class DiagnosesFormValidator(ReportingFieldsetFormValidatorMixin, FormValidator):
    def clean(self) -> None:
        # TODO: validate reporting na if no dx
        self.validate_reporting_fieldset_na_baseline()


class DiagnosesForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = DiagnosesFormValidator

    class Meta:
        model = Diagnoses
        fields = "__all__"
