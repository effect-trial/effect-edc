from django import forms
from edc_form_validators import FormValidatorMixin
from edc_model_form.mixins import BaseModelFormMixin
from edc_sites.modelform_mixins import SiteModelFormMixin
from effect_form_validators.effect_reports import (
    ScreeningCragDateConfirmationFormValidator,
)

from ..models import ScreeningCragDateConfirmation


class ScreeningCragDateConfirmationForm(
    SiteModelFormMixin,
    # RequiresConsentModelFormMixin,  # screening date < consent date
    # VisitScheduleCrfModelFormMixin,
    # VisitTrackingCrfModelFormMixin,
    # OffstudyCrfModelFormMixin,
    BaseModelFormMixin,
    FormValidatorMixin,
    forms.ModelForm,
):
    form_validator_cls = ScreeningCragDateConfirmationFormValidator

    class Meta:
        model = ScreeningCragDateConfirmation
        fields = "__all__"
        labels = {
            "confirmed_gender": "Sex",
        }
        widgets = {
            "screening_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
        }
