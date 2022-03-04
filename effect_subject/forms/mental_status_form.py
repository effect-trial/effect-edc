from django import forms
from edc_constants.constants import NOT_APPLICABLE
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator
from edc_visit_schedule.utils import is_baseline

from ..models import MentalStatus


class MentalStatusFormValidator(FormValidator):
    def clean(self) -> None:
        for reportable_field in ["reportable_as_ae", "patient_admitted"]:
            self.applicable_if_true(
                condition=not is_baseline(self.cleaned_data.get("subject_visit")),
                not_applicable_msg="Expected 'Not applicable' at baseline.",
                field_applicable=reportable_field,
            )


class MentalStatusForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = MentalStatusFormValidator

    class Meta:
        model = MentalStatus
        fields = "__all__"
