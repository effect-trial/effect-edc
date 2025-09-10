from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_crf.modelform_mixins import CrfModelFormMixin
from effect_form_validators.effect_subject import SignsAndSymptomsFormValidator as Base

from effect_lists.list_data import list_data
from effect_lists.models import SiSx

from ..models import SignsAndSymptoms


class SignsAndSymptomsFormValidator(Base):
    @staticmethod
    def _get_sisx_display_value(key):
        return dict(list_data["effect_lists.sisx"])[key]


class SignsAndSymptomsForm(CrfModelFormMixin, ActionItemFormMixin, forms.ModelForm):
    form_validator_cls = SignsAndSymptomsFormValidator

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.fields.get("current_sx"):
            self.fields["current_sx"].queryset = SiSx.objects.order_by("display_index")
        if self.fields.get("current_sx_gte_g3"):
            self.fields["current_sx_gte_g3"].queryset = SiSx.objects.order_by("display_index")

    class Meta:
        model = SignsAndSymptoms
        fields = "__all__"
