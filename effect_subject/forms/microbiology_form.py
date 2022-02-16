from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_microbiology.form_validators import MicrobiologyFormValidator

from ..models import Microbiology


class MicrobiologyForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = MicrobiologyFormValidator

    class Meta:
        model = Microbiology
        fields = "__all__"
