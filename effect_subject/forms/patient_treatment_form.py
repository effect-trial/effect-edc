from django import forms
from edc_constants.constants import NO, OTHER, YES
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator

from ..models import PatientTreatment


class PatientTreatmentFormValidator(FormValidator):
    def clean(self):
        self.validate_cm_tx()
        self.validate_tb_tx()
        self.validate_steroids()
        self.validate_co_trimoxazole()
        self.validate_antibiotics()
        self.validate_other_drugs()

    def validate_cm_tx(self):
        self.applicable_if(YES, field="lp_completed", field_applicable="cm_confirmed")
        self.applicable_if(YES, field="cm_confirmed", field_applicable="cm_tx")
        self.applicable_if(YES, field="cm_tx", field_applicable="cm_tx_given")
        self.validate_other_specify("cm_tx_given")

    def validate_tb_tx(self):
        self.required_if(YES, field="tb_tx", field_required="tb_tx_date")
        self.m2m_required_if(YES, field="tb_tx", m2m_field="tb_tx_given")
        self.m2m_other_specify(
            OTHER, m2m_field="tb_tx_given", field_other="tb_tx_given_other"
        )
        self.applicable_if(NO, field="tb_tx", field_applicable="tb_tx_reason_no")
        self.validate_other_specify("tb_tx_reason_no")

    def validate_steroids(self):
        self.required_if(YES, field="steroids", field_required="steroids_date")
        self.applicable_if(YES, field="steroids", field_applicable="steroids_given")
        self.validate_other_specify("steroids_given")
        self.required_if(YES, field="steroids", field_required="steroids_course")

    def validate_co_trimoxazole(self):
        self.required_if(
            YES, field="co_trimoxazole", field_required="co_trimoxazole_date"
        )
        self.applicable_if(
            NO, field="co_trimoxazole", field_applicable="co_trimoxazole_reason_no"
        )
        self.validate_other_specify("co_trimoxazole_reason_no")

    def validate_antibiotics(self):
        self.required_if(YES, field="antibiotics", field_required="antibiotics_date")
        self.m2m_required_if(YES, field="antibiotics", m2m_field="antibiotics_given")
        self.m2m_other_specify(
            OTHER, m2m_field="antibiotics_given", field_other="antibiotics_given_other"
        )

    def validate_other_drugs(self):
        self.required_if(YES, field="other_drugs", field_required="other_drugs_date")
        self.m2m_required_if(YES, field="other_drugs", m2m_field="other_drugs_given")
        self.m2m_other_specify(
            OTHER, m2m_field="other_drugs_given", field_other="other_drugs_given_other"
        )


class PatientTreatmentForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = PatientTreatmentFormValidator

    class Meta:
        model = PatientTreatment
        fields = "__all__"
