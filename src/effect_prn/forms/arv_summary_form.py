from clinicedc_constants import NO, YES
from django import forms
from edc_form_validators import FormValidator, FormValidatorMixin
from edc_model_form.mixins import BaseModelFormMixin
from edc_sites.forms import SiteModelFormMixin

from ..models import ArvSummary


class ArvSummaryFormValidator(FormValidator):
    """Not used"""

    def clean(self):
        self.required_if(YES, field="at_screening", field_required="at_screening_regimen")
        self.applicable_if(
            YES, field="at_screening", field_applicable="at_screening_start_date_known"
        )
        self.required_if(
            YES,
            field="at_screening_start_date_known",
            field_required="at_screening_start_date",
        )

        self.applicable_if(YES, field="at_screening", field_applicable="cont_enrol")

        self.applicable_if(YES, field="cont_enrol", field_applicable="cont_enrol_changed")
        self.applicable_if(
            YES, field="cont_enrol_changed", field_applicable="cont_enrol_regimen"
        )

        cond = self.cleaned_data.get("at_screening") == NO or (
            self.cleaned_data.get("at_screening") == YES
            and self.cleaned_data.get("cont_enrol") == NO
        )
        self.applicable_if_true(cond, field_applicable="after_enrol")
        self.applicable_if(YES, field="after_enrol", field_applicable="after_enrol_regimen")
        self.applicable_if(
            YES, field="after_enrol", field_applicable="after_enrol_start_date_known"
        )
        self.required_if(
            YES,
            field="after_enrol_start_date_known",
            field_required="after_enrol_start_date",
        )


class ArvSummaryForm(
    SiteModelFormMixin,
    FormValidatorMixin,
    BaseModelFormMixin,
    forms.ModelForm,
):
    form_validator_cls = ArvSummaryFormValidator

    class Meta:
        model = ArvSummary
        fields = "__all__"
