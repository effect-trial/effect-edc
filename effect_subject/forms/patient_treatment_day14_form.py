from django import forms
from edc_constants.constants import OTHER
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator

from ..models import PatientTreatmentDay14


class PatientTreatmentDay14FormValidator(FormValidator):
    def clean(self):
        self.m2m_other_specify(
            OTHER,
            m2m_field="other_antibiotics_first_2w",
            field_other="other_antibiotics_first_2w_other",
        )

        self.m2m_other_specify(
            OTHER,
            m2m_field="other_drugs_first_2w",
            field_other="other_drugs_first_2w_other",
        )

        protocol_fcon_rx_d14 = 800
        self.required_if_true(
            condition=self.cleaned_data.get("fcon_rx_d14") != protocol_fcon_rx_d14,
            field_required="fcon_rx_d14_reason",
        )


class PatientTreatmentDay14Form(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = PatientTreatmentDay14FormValidator

    class Meta:
        model = PatientTreatmentDay14
        fields = "__all__"
