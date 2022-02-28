from django import forms
from edc_constants.constants import POS, YES
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import FormValidator

from ..models import Histopathology


class HistopathologyFormValidatorMixin:
    def validate_histopathology(self: FormValidator):
        self.required_if(
            YES, field="tissue_biopsy_performed", field_required="tissue_biopsy_date"
        )
        self.applicable_if(
            YES,
            field="tissue_biopsy_performed",
            field_applicable="tissue_biopsy_result",
        )
        self.required_if(
            POS,
            field="tissue_biopsy_result",
            field_required="tissue_biopsy_organism_text",
        )


class HistopathologyFormValidator(
    HistopathologyFormValidatorMixin,
    FormValidator,
):
    def clean(self):
        self.validate_histopathology()


class HistopathologyForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = HistopathologyFormValidator

    class Meta:
        model = Histopathology
        fields = "__all__"
