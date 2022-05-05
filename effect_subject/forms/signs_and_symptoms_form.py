from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_crf.modelform_mixins import CrfModelFormMixin
from effect_form_validators.effect_subject import SignsAndSymptomsFormValidator as Base

from effect_lists.list_data import list_data

from ..models import SignsAndSymptoms


class SignsAndSymptomsFormValidator(Base):
    @staticmethod
    def _get_sisx_display_value(key):
        return dict(list_data["effect_lists.sisx"])[key]


class SignsAndSymptomsForm(CrfModelFormMixin, ActionItemFormMixin, forms.ModelForm):
    form_validator_cls = SignsAndSymptomsFormValidator

    class Meta:
        model = SignsAndSymptoms
        fields = "__all__"
