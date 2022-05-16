from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_form_validators import FormValidatorMixin
from edc_sites.forms import SiteModelFormMixin
from effect_form_validators.effect_prn import HospitalizationFormValidator as Base

from ..models import Hospitalization


class HospitalizationFormValidator(Base):
    pass


class HospitalizationForm(
    SiteModelFormMixin,
    FormValidatorMixin,
    ActionItemFormMixin,
    forms.ModelForm,
):

    form_validator_cls = HospitalizationFormValidator

    subject_identifier = forms.CharField(
        label="Subject Identifier",
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )

    class Meta:
        model = Hospitalization
        fields = "__all__"
