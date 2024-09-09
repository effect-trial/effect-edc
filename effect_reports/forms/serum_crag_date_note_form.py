from django import forms
from edc_form_validators import FormValidatorMixin
from edc_model_form.mixins import BaseModelFormMixin
from edc_sites.modelform_mixins import SiteModelFormMixin
from effect_form_validators.effect_reports import SerumCragDateNoteFormValidator

from ..models import SerumCragDateNote


class SerumCragDateNoteForm(
    SiteModelFormMixin,
    BaseModelFormMixin,
    FormValidatorMixin,
    forms.ModelForm,
):

    report_datetime_field_attr = "report_datetime"
    form_validator_cls = SerumCragDateNoteFormValidator

    class Meta:
        model = SerumCragDateNote
        fields = "__all__"
        help_text = {"subject_identifier": "(read-only)", "name": "(read-only)"}
        widgets = {
            "report_model": forms.TextInput(attrs={"readonly": "readonly"}),
            "subject_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
            "name": forms.TextInput(attrs={"readonly": "readonly"}),
        }
