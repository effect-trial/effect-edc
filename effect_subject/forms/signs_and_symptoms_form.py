from django import forms
from edc_constants.constants import YES
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator

from ..constants import HEADACHE, VISUAL_LOSS
from ..models import SignsAndSymptoms


class SignsAndSymptomsFormValidator(FormValidator):
    def clean(self) -> None:
        # TODO: Validate that patient can't specify UNKNOWN for
        #  any_signs_symptoms (e.g. if an in-person or telephone/patient visit)

        self.m2m_required_if(
            response=YES,
            field="any_signs_symptoms",
            m2m_field="signs_and_symptoms",
        )

        self.applicable_if(
            YES, field="any_signs_symptoms", field_applicable="reportable_as_ae"
        )
        self.m2m_required_if(
            response=YES,
            field="reportable_as_ae",
            m2m_field="signs_and_symptoms_gte_g3",
        )

        # TODO: test signs_and_symptoms_gte_g3 specified are a subset of
        #  those specified in signs_and_symptoms

        self.m2m_other_specify(
            HEADACHE, m2m_field="signs_and_symptoms", field_other="headache_duration"
        )

        self.m2m_other_specify(
            VISUAL_LOSS, m2m_field="signs_and_symptoms", field_other="visual_field_loss"
        )

        self.applicable_if(
            YES, field="any_signs_symptoms", field_applicable="patient_admitted"
        )
        self.applicable_if(
            YES, field="any_signs_symptoms", field_applicable="cm_signs_symptoms"
        )


class SignsAndSymptomsForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = SignsAndSymptomsFormValidator

    class Meta:
        model = SignsAndSymptoms
        fields = "__all__"
