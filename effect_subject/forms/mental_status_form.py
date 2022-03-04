from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator

from ..models import MentalStatus
from .mixins import ReportingFieldsetFormValidatorMixin


class MentalStatusFormValidator(ReportingFieldsetFormValidatorMixin, FormValidator):
    def clean(self) -> None:
        self.validate_reporting_fieldset()


class MentalStatusForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = MentalStatusFormValidator

    class Meta:
        model = MentalStatus
        fields = "__all__"
