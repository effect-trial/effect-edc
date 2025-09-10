from django import forms
from edc_action_item.forms import ActionItemCrfFormMixin
from edc_constants.choices import YES_NO
from edc_crf.modelform_mixins import CrfModelFormMixin
from effect_form_validators.effect_subject import VitalSignsFormValidator

from ..models import VitalSigns


class VitalSignsForm(CrfModelFormMixin, ActionItemCrfFormMixin, forms.ModelForm):
    form_validator_cls = VitalSignsFormValidator

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.fields.get("reportable_as_ae"):
            self.fields["reportable_as_ae"].choices = YES_NO
        if self.fields.get("patient_admitted"):
            self.fields["patient_admitted"].choices = YES_NO

    class Meta(ActionItemCrfFormMixin.Meta):
        model = VitalSigns
        fields = "__all__"
