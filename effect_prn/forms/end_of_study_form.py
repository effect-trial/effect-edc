from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_form_validators import FormValidatorMixin
from edc_model_form.mixins import BaseModelFormMixin
from edc_sites.forms import SiteModelFormMixin
from edc_visit_schedule.modelform_mixins import OffScheduleModelFormMixin

from ..form_validators import EndOfStudyFormValidator
from ..models import EndOfStudy


class EndOfStudyForm(
    SiteModelFormMixin,
    ActionItemFormMixin,
    OffScheduleModelFormMixin,
    BaseModelFormMixin,
    FormValidatorMixin,
    forms.ModelForm,
):
    form_validator_cls = EndOfStudyFormValidator

    report_datetime_field_attr: str = "offschedule_datetime"

    class Meta(ActionItemFormMixin.Meta):
        model = EndOfStudy
        fields = "__all__"
