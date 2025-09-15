from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from effect_form_validators.effect_subject import LpCsfFormValidator as Base

from effect_labs.panels import csf_culture_panel

from ..models import LpCsf


class LpCsfFormValidator(Base):
    csf_culture_panel = csf_culture_panel


class LpCsfForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = LpCsfFormValidator

    class Meta:
        model = LpCsf
        fields = "__all__"
