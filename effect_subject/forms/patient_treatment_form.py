from django import forms
from edc_constants.constants import OTHER, YES
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator

from ..models import PatientTreatment


class PatientTreatmentFormValidator(FormValidator):
    def clean(self):
        super().clean()

        self.validate_cm_tx()

        self.m2m_other_specify(
            OTHER, m2m_field="tb_tx_given", field_other="tb_tx_given_other"
        )

        self.validate_steroids_administered()

        self.m2m_other_specify(
            OTHER, m2m_field="antibiotics_given", field_other="antibiotics_given_other"
        )

    def validate_cm_tx(self):
        self.applicable_if(YES, field="lp_completed", field_applicable="cm_confirmed")
        self.applicable_if(YES, field="cm_confirmed", field_applicable="cm_tx")
        self.applicable_if(YES, field="cm_tx", field_applicable="cm_tx_given")
        self.validate_other_specify("cm_tx_given")

    def validate_steroids_administered(self):
        self.applicable_if(YES, field="steroids", field_applicable="steroids_given")
        self.validate_other_specify("steroids_given")
        self.required_if(
            YES,
            field="steroids",
            field_required="steroids_course",
        )


class PatientTreatmentForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = PatientTreatmentFormValidator

    class Meta:
        model = PatientTreatment
        fields = "__all__"
