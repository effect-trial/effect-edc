from django import forms
from edc_constants.constants import NO, YES
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_csf.form_validators import LpCsfFormValidator as BaseLpCsfFormValidator
from edc_form_validators import FormValidator

from effect_labs.panels import csf_culture_panel

from ..models import LpCsf


class LpCsfFormValidator(BaseLpCsfFormValidator):
    def clean(self):

        self.validate_lp()

        self.validate_csf_assessment()

        self.validate_csf_culture("csf_requisition")

    def validate_csf_assessment(self: FormValidator):
        for fld in [
            "india_ink",
            "csf_crag_lfa",
            "sq_crag",
            "sq_crag_pos",
            "crf_crag_titre_done",
        ]:
            self.applicable_if(YES, NO, field="csf_positive", field_applicable=fld)

        self.required_if(
            YES, field="crf_crag_titre_done", field_required="crf_crag_titre"
        )

    def validate_csf_culture(self: FormValidator, requisition: str):
        self.require_together(
            field=requisition,
            field_required="csf_assay_datetime",
        )
        self.validate_requisition(requisition, "csf_assay_datetime", csf_culture_panel)
        self.required_if_true(
            self.cleaned_data.get("quantitative_culture") is not None,
            field_required=requisition,
        )


class LpCsfForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = LpCsfFormValidator

    class Meta:
        model = LpCsf
        fields = "__all__"
