from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_form_validators import FormValidatorMixin
from edc_sites.forms import SiteModelFormMixin
from edc_visit_schedule.modelform_mixins import OffScheduleModelFormMixin

from ..form_validators import EndOfStudyFormValidator
from ..models import EndOfStudy


class EndOfStudyForm(
    SiteModelFormMixin,
    FormValidatorMixin,
    ActionItemFormMixin,
    OffScheduleModelFormMixin,
    forms.ModelForm,
):

    form_validator_cls = EndOfStudyFormValidator

    subject_identifier = forms.CharField(
        label="Subject Identifier",
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )

    class Meta:
        model = EndOfStudy
        fields = "__all__"
        help_texts = {
            "offschedule_datetime": "This can include date of: lost to follow up; withdrawal, Death, Calendar month 6",
            "missed_doses_5fc_cnt": "If no missed doses, Enter 0",
            "missed_doses_flu_cnt": "If no missed doses, Enter 0",
            "missed_doses_consolidation_flu_cnt": "If no missed doses, Enter 0",
        }
